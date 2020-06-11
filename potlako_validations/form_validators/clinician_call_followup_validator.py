from edc_constants.constants import YES
from edc_form_validators import FormValidator
from .crf_form_validator import CRFFormValidator


class ClinicianCallFollowupFormValidator(CRFFormValidator, FormValidator):

    def clean(self):

        self.subject_identifier = self.cleaned_data.get(
            'subject_visit').appointment.subject_identifier

        self.validate_other_specify('facility_visited',)

        self.validate_other_specify('facility_unit',)

        referral_fields = ['referral_date', 'referral_facility',
                           'referral_reason', 'referral_discussed', ]

        for field in referral_fields:
            self.required_if(
                'refer',
                field='patient_disposition',
                field_required=field
            )

        self.required_if(
            YES,
            field='referral_discussed',
            field_required='referral_discussed_clinician')

        self.not_required_if(
            'discharge',
            field='patient_disposition',
            field_required='return_visit_scheduled'
        )

        self.required_if(
            YES,
            field='return_visit_scheduled',
            field_required='return_visit_date'
        )

        self.validate_next_appointment_date(
            next_ap_date=self.cleaned_data.get('return_visit_date'))

        super().clean()
