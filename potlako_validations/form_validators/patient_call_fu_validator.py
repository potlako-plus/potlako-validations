from datetime import datetime
import pytz
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django.utils import timezone
from edc_action_item.site_action_items import site_action_items
from edc_constants.constants import NO, YES, OPEN
from edc_form_validators import FormValidator

from potlako_subject.action_items import UPDATE_LOCATOR_ACTION


class PatientCallFuFormValidator(FormValidator):

    subject_locator_model = 'potlako_subject.subjectlocator'

    @property
    def subject_locator_model_cls(self):
        return django_apps.get_model(self.subject_locator_model)

    @property
    def facility_app_config(self):
        return django_apps.get_app_config('edc_facility')

    def clean(self):
        fields = ['visit_delayed_count', 'visit_delayed_reason',
                  'patient_factor', 'health_system_factor',
                  'delayed_visit_description', ]
        for field in fields:
            if field in self.cleaned_data:
                self.not_required_if(
                    NO,
                    field='next_visit_delayed',
                    field_required=field,)

        fields = {'new_complaints': 'new_complaints_description',
                  'appt_change': 'appt_change_reason'}

        for field, required_field in fields.items():
            self.required_if(
                YES,
                field=field,
                field_required=required_field)

        self.validate_other_specify(
            'next_ap_facility',
            other_specify_field='next_ap_facility_other',)

        self.validate_next_appointment_date_valid()

        residence_change = self.cleaned_data.get('patient_residence_change')
        next_kin_contact_change = self.cleaned_data.get(
            'next_kin_contact_change')
        if residence_change == YES and next_kin_contact_change == YES:
            subject_visit = self.cleaned_data.get('subject_visit')
            subject_identifier = subject_visit.subject_identifier

#             self.get_subject_locator_or_message(
#                 subject_identifier=subject_identifier)

    def get_subject_locator_or_message(self, subject_identifier=None):
        try:
            self.subject_locator_model_cls.objects.get(
                subject_identifier=subject_identifier)
        except self.subject_locator_model_cls.DoesNoExist:
            msg = {'__all__': 'Subject Locator not found, please add '
                   'Locator before proceeding.'}
            self._errors.update(msg)
            raise ValidationError(msg)
        else:
            action_cls = site_action_items.get(
                self.subject_locator_model_cls.action_name)
            action_item_model_cls = action_cls.action_item_model_cls()
            try:
                action_item_model_cls.objects.get(
                    subject_identifier=subject_identifier,
                    action_type__name=UPDATE_LOCATOR_ACTION)
            except action_item_model_cls.DoesNotExist:
                action_cls(
                    subject_identifier=subject_identifier)

    def validate_next_appointment_date_valid(self):
        next_ap_date = self.cleaned_data.get('next_appointment_date')
        subject_visit = self.cleaned_data.get('subject_visit')

        if next_ap_date:
            my_time = datetime.min.time()
            suggested_datetime = datetime.combine(next_ap_date, my_time)
            suggested_datetime = timezone.make_aware(
                suggested_datetime, timezone=pytz.utc)

            facility = self.get_facility(subject_visit=subject_visit)
            available_datetime = facility.available_rdate(suggested_datetime)

            # Change suggested datetime to arrow before compare
            if next_ap_date != available_datetime:
                msg = {'next_appointment_date':
                       f'{next_ap_date} falls on a holiday/weekend, please specify'
                       ' a different date. Next available date is '
                       f'{available_datetime.format("dddd")}, '
                       f'{available_datetime.format("DD-MM-YYYY")}'}
                self._errors.update(msg)
                raise ValidationError(msg)

    def get_facility(self, subject_visit=None):
        facility_name = subject_visit.appointment.facility_name
        return self.facility_app_config.get_facility(facility_name)
