from edc_form_validators import FormValidator


class ClinicianCallFollowupFormValidator(FormValidator):

    def clean(self):
        super().clean()

        self.validate_other_specify('facility_visited',)

        self.validate_other_specify('facility_unit',)

        referral_fields = ['referral_date', 'referral_facility',
                           'referral_reason', 'referral_discussed',
                           'referral_discussed_clinician', ]

        for field in referral_fields:
            self.required_if(
                'refer',
                field='patient_disposition',
                field_required=field
            )

        self.not_required_if(
            'discharge',
            field='patient_disposition',
            field_required='return_visit_date'
        )
