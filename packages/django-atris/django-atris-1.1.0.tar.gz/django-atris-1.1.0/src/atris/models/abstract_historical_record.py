# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import logging
from datetime import timedelta

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField, JSONField
from django.core.exceptions import FieldDoesNotExist
from django.db import models, connection
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils import six
from django.utils.timezone import now

from .helpers import get_diff_fields


str = unicode if six.PY2 else str


logger = logging.getLogger(__name__)


class HistoricalRecordQuerySet(QuerySet):

    def by_model_and_model_id(self, model, model_id):
        """
        Gets historical records by model and model id, so, basically the
        historical records for an instance of a model.
        :param model: Model which has the HistoricalRecord field.
        :param model_id: The model id for which you wish to get the history.
        :return: The instance's history.
        :rtype HistoricalRecord
        """
        return self.by_model(model).filter(object_id=model_id)

    def by_model_proxy_and_id(self, model_proxy, id_):
        """
        When saving history for a Model Proxy, some information (especially
        the related history) will be saved with the ContentType of the
        concrete model. This method will return entries for both the proxy and
        the concrete model with the given object ID.
        """
        concrete_model = model_proxy._meta.concrete_model
        by_models = self.filter(
            Q(content_type__model=model_proxy._meta.model_name) &
            Q(content_type__app_label=model_proxy._meta.app_label) |
            Q(content_type__model=concrete_model._meta.model_name) &
            Q(content_type__app_label=concrete_model._meta.app_label)
        )
        return by_models.filter(object_id=id_)

    def by_model(self, model):
        # noinspection PyProtectedMember
        """
        Gets historical records by model.
        :param model: Model which has the HistoricalRecord field.
        :return: The entire model's history.
        :rtype HistoricalRecord
        """
        return self.filter(
            content_type__model=model._meta.model_name,
            content_type__app_label=model._meta.app_label
        )

    def by_app_label_and_model_name(self, app_label, model_name):
        """
        Gets historical record by app label and model name.
        :param app_label: The name of the application in which the model is
        defined.
        :param model_name: The name of the model that has a HistoricalRecord
        field.
        :return: The entire history of the model.
        """
        return self.filter(
            content_type__model=model_name,
            content_type__app_label=app_label
        )

    def most_recent(self):
        """
        Gets the most recent historical record added to the database.
        :return: The most recent historical record added to the database.
        :rtype HistoricalRecord
        """
        return self.first()

    def older_than(self, days=None, weeks=None):
        """
        Gets all historical record entries that are older than either the
        number of days or the number of weeks passed.
        The weeks parameter will be preferred if both are supplied.
        :param days: Number of days old a historical record can be, at most.
        :param weeks: Number of weeks old a historical record can be, at most.
        :return: All the historical record entries that are older than the
                 given param.
        :rtype list(HistoricalRecord)
        """
        if not (days or weeks):
            logger.error('You must supply either the days or the weeks param')
            return
        elif days and weeks:
            logger.info('You supplied both days and weeks, weeks param'
                        ' will be used as the delimiter.')
        td = timedelta(weeks=weeks) if weeks else timedelta(days=days)
        return self.filter(history_date__lte=now() - td)

    def previous_version_by_model_and_id(self, model, object_id, history_id):
        """
        Returns the second to last snapshot of the history for model and
        instance id that is given.
        :param history_id: Id for history snapshot.
        :param model: The model for which the snapshot is for.
        :param object_id: The model ID for which the snapshot is for.
        :return: The previous to HistoricalRecord

        """
        main_qs = self.filter(
            content_type__model=model.model,
            content_type__app_label=model.app_label,
            object_id=object_id,
            id__lt=history_id
        )
        return main_qs.order_by('-history_date').first()

    def approx_count(self):
        """
            Takes a queryset and generates a fast approximate count(*) for it.
            This is required because postgresql count(*) has to go through all
            of the entries in the database, making it extremely slow for
            large tables.
            :return: int representing approx count(*)
            """
        table_name = self.model._meta.db_table
        cursor = connection.cursor()
        cursor.execute(
            "SELECT reltuples FROM pg_class WHERE relname='{}';".format(
                table_name))
        row = cursor.fetchone()
        return int(row[0])


class AbstractHistoricalRecord(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = GenericForeignKey(
        'content_type',
        'object_id',
        for_concrete_model=False
    )

    history_date = models.DateTimeField(auto_now_add=True, db_index=True)
    history_user = models.CharField(max_length=50, null=True)
    history_user_id = models.PositiveIntegerField(null=True)
    history_type = models.CharField(
        max_length=1,
        choices=(
            ('+', 'Create'),
            ('~', 'Update'),
            ('-', 'Delete'),
        ),
        db_index=True
    )
    history_diff = ArrayField(models.CharField(max_length=200),
                              blank=True, null=True)

    data = JSONField()
    related_field_history = models.ForeignKey(
        'self',
        related_name='referenced_objects_history',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    additional_data = JSONField(null=True)
    objects = HistoricalRecordQuerySet.as_manager()

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return '{history_type} {content_type} id={object_id}'.format(
            history_type=self.get_history_type_display(),
            content_type=self.content_type.model,
            object_id=self.object_id
        )

    class Meta:
        app_label = 'atris'
        ordering = ['-history_date']
        abstract = True

    def get_diff_to_prev_string(self):
        """
        Generates a string which describes the changes that occurred between
        this historical record instance (self) and its previous version.

        :return: Said string.
        :rtype String
        """
        # Recalculating diff in case the missing history has been
        # generated/restored.
        if self.history_diff is None:
            self._regenerate_history_diff()
        diff_string = '{}d '.format(self.get_history_type_display())
        if self.history_type == '~':
            if self.history_diff is None:
                diff_string = 'No prior information available.'
            elif not self.history_diff:
                diff_string += 'with no change'
            else:
                verbose_names = [
                    self._get_field_name_display(field_name)
                    for field_name in self.history_diff
                ]
                diff_string += ', '.join(sorted(verbose_names))
        else:
            diff_string += self.content_type.name
        return diff_string

    def _get_field_name_display(self, field_name):
        model = self.content_type.model_class()
        try:
            field = model._meta.get_field(field_name)
        except FieldDoesNotExist:
            return field_name.replace('_', ' ').title()
        if hasattr(field, 'verbose_name'):
            return field.verbose_name
        else:
            return field.name.replace('_', ' ').title()

    def _regenerate_history_diff(self):
        previous_data = getattr(self._get_prev_version(), 'data', None)
        tracked_model = self.content_type.model_class()
        excluded_fields = (tracked_model._meta.history_logging
                           .excluded_fields_names)
        self.history_diff = get_diff_fields(tracked_model, self.data,
                                            previous_data, excluded_fields)
        self.save(update_fields=['history_diff'])

    def _get_prev_version(self):
        return self.__class__.objects.previous_version_by_model_and_id(
            model=self.content_type,
            object_id=self.object_id,
            history_id=self.id
        )
