import arrow
import pytz
from datetime import datetime
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django.utils import timezone
from edc_constants.constants import NO, YES
from edc_form_validators import FormValidator


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

    def validate_next_appointment_date_valid(self):
        next_ap_date = self.cleaned_data.get('next_appointment_date')
        subject_visit = self.cleaned_data.get('subject_visit')

        if next_ap_date:
            my_time = datetime.min.time()
            suggested_datetime = datetime.combine(next_ap_date, my_time)
            suggested_datetime = timezone.make_aware(
                suggested_datetime, timezone=pytz.utc)

            facility = self.get_facility(subject_visit=subject_visit)
            available_datetime = facility.available_rdate(
                suggested_datetime=suggested_datetime, )

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
