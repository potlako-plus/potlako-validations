from datetime import datetime

import arrow
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django.utils import timezone
from edc_constants.constants import NO, YES
from edc_form_validators import FormValidator
import pytz


class MissedVisitFormValidator(FormValidator):

    @property
    def facility_app_config(self):
        return django_apps.get_app_config('edc_facility')

    def clean(self):

        self.required_if(
            NO,
            field='inquired',
            field_required='not_inquired_reason')

        self.required_if(
            NO,
            field='transport_support',
            field_required='transport_need')

        self.required_if(
            YES,
            field='inquired',
            field_required='inquired_from')

        other_fields = ['facility_scheduled', 'determine_missed',
                        'not_inquired_reason', 'reason_missed',
                        'next_ap_facility', 'clinician_designation']
        for field in other_fields:
            self.validate_other_specify(field)

        self.validate_next_appointment_date()

    def validate_next_appointment_date(self):
        next_ap_date = self.cleaned_data.get('next_appointment')
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
