from edc_constants.constants import YES
from edc_form_validators import FormValidator

from .crf_form_validator import CRFFormValidator
from .form_validator_mixin import FormValidatorMixin


class ClinicianCallEnrollmentFormValidator(FormValidator):

    def clean(self):

        self.validate_other_specify(
            field='call_clinician_type',
            other_specify_field='call_clinician_other',
        )

        self.validate_other_specify(field='facility',)

        self.validate_other_specify(
            field='facility_unit',
            other_specify_field='unit_other'
        )

        self.validate_other_specify(field='nearest_facility',)

        self.validate_other_specify(
            field='kin_relationship',
            other_specify_field='kin_relation_other'
        )

        self.validate_other_specify(
            field='clinician_type',
            other_specify_field='clinician_other'
        )

        self.validate_other_specify(field='symptoms',)

        self.required_if(
            YES,
            field='early_symptoms_date_estimated',
            field_required='early_symptoms_date_estimation'
        )

        self.validate_other_specify(field='suspected_cancer',)

        referral_fields = ['referral_reason', 'referral_date',
                           'referral_facility', 'referral_unit',
                           'referral_discussed', 'clinician_designation',
                           'referral_fu_date', ]

        for field in referral_fields:
            self.required_if(
                'refer',
                field='patient_disposition',
                field_required=field
            )

        self.validate_other_specify(field='referral_facility',)

        for field in referral_fields:
            self.required_if(
                YES,
                field='investigated',
                field_required='notes'
            )

