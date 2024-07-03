from datetime import datetime

import arrow
from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django.utils import timezone
from edc_action_item.site_action_items import site_action_items
from edc_constants.constants import NO, NEW
from potlako_prn.action_items import SUBJECT_OFFSTUDY_ACTION
from django.core.exceptions import ObjectDoesNotExist
import pytz


class CRFFormValidator:

    @property
    def facility_app_config(self):
        return django_apps.get_app_config('edc_facility')

    def clean(self):
        if not self.cleaned_data.get('subject_visit'):
            raise forms.ValidationError(
                "Missing Subject Visit.")

        if self.instance and not self.instance.id:
            self.validate_cancer_dx_endpoint()
        super().clean()

    # check cancerdxandtxendpoint
    def validate_cancer_dx_endpoint(self):
        """Checks if there is a cancer endpoint to mark offstudy
        """
        cancer_dx_endpoint_cls = django_apps.get_model('potlako_subject.cancerdxandtxendpoint')
        try:
            obj = cancer_dx_endpoint_cls.objects.get(
                subject_identifier=self.subject_identifier)
        except ObjectDoesNotExist:
            pass
        else:
            if obj.final_deposition == 'exit':
                raise forms.ValidationError(
                        'Participant has been taken offstudy. Cannot capture any '
                        'new data.')

    def validate_offstudy_model(self):
        subject_offstudy_cls = django_apps.get_model(
            'potlako_prn.subjectoffstudy')
        action_cls = site_action_items.get(
            subject_offstudy_cls.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()

        try:
            action_item_model_cls.objects.get(
                subject_identifier=self.subject_identifier,
                action_type__name=SUBJECT_OFFSTUDY_ACTION,
                status=NEW)
        except action_item_model_cls.DoesNotExist:
            try:
                subject_offstudy_cls.objects.get(
                    subject_identifier=self.subject_identifier)
            except subject_offstudy_cls.DoesNotExist:
                pass
            else:
                raise forms.ValidationError(
                    'Participant has been taken offstudy. Cannot capture any '
                    'new data.')
        else:
            self.subject_visit = self.cleaned_data.get('subject_visit') or None
            if not self.subject_visit or self.subject_visit.require_crfs == NO:
                raise forms.ValidationError(
                    'Participant is scheduled to be taken offstudy without '
                    'any new data collection. Cannot capture any new data.')

    def validate_next_appointment_date(self, next_ap_date=None,):
        subject_visit = self.cleaned_data.get('subject_visit')

        if next_ap_date:
            my_time = datetime.min.time()
            suggested_datetime = datetime.combine(next_ap_date, my_time)
            suggested_datetime = timezone.make_aware(
                suggested_datetime, timezone=pytz.utc)

            facility = self.get_facility(subject_visit=subject_visit)
            available_datetime = facility.available_rdate(
                suggested_datetime=suggested_datetime,)

            # Change suggested datetime to arrow before compare
            suggested_rdate = arrow.Arrow.fromdatetime(suggested_datetime)
            if suggested_rdate != available_datetime:
                msg = {'next_appointment_date':
                       f'{next_ap_date} falls on a holiday/weekend, please '
                       'specify a different date. Next available date is '
                       f'{available_datetime.format("dddd")}, '
                       f'{available_datetime.format("DD-MM-YYYY")}'}
                self._errors.update(msg)
                raise ValidationError(msg)

    def get_facility(self, subject_visit=None):
        facility_name = subject_visit.appointment.facility_name
        return self.facility_app_config.get_facility(facility_name)
