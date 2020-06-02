from edc_constants.constants import NO, YES
from edc_form_validators import FormValidator
from .crf_form_validator import CRFFormValidator


class MissedVisitFormValidator(CRFFormValidator, FormValidator):

    def clean(self):

        self.subject_identifier = self.cleaned_data.get(
            'subject_visit').appointment.subject_identifier

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

        self.validate_next_appointment_date(
            next_ap_date=self.cleaned_data.get('next_appointment'))

        super().clean()
