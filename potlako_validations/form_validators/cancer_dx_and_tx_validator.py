from edc_constants.constants import YES

from edc_form_validators import FormValidator


class CancerDxAndTxFormValidator(FormValidator):

    def clean(self):

        req_fields = ['diagnosis_date', 'diagnosis_date_estimated']
        for req_field in req_fields:
            self.required_if(
                'complete',
                field='cancer_evaluation',
                field_required=req_field)

        fields_required = {
            'diagnosis_date_estimated': 'diagnosis_date_estimation',
            'cancer_treatment': 'treatment_description'}

        for field, field_required in fields_required.items():
            self.required_if(
                YES,
                field=field,
                field_required=field_required)
