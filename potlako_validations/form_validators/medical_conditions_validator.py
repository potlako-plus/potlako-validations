from edc_constants.constants import YES
from edc_form_validators import FormValidator
from .crf_form_validator import CRFFormValidator


class MedicalConditionsFormValidator(CRFFormValidator, FormValidator):

    def clean(self):
        super().clean()

        self.required_if(
            YES,
            field='diagnosis_date_estimate',
            field_required='diagnosis_date_estimation',)

        self.required_if(
            YES,
            field='on_medication',
            field_required='treatment_type',)

        self.required_if(
            YES,
            field='on_medication',
            field_required='treatment_name',)

        self.validate_other_specify(
            'medical_condition')
