from edc_constants.constants import YES
from edc_form_validators import FormValidator


class SymptomAndCareSeekingFormValidator(FormValidator):

    def clean(self):

        self.validate_other_specify(field='symptoms_present')

        fields_required = ['discussion_person', 'discussion_date',
                           'medical_advice', 'discussion_date_estimated']

        for field_required in fields_required:
            self.required_if(
                YES,
                field='symptoms_discussion',
                field_required=field_required)

        self.validate_other_specify(field='discussion_person')

        req_fields = {
            'discussion_date_estimated': 'discussion_date_estimation',
            'clinic_visit_date_estimated': 'clinic_visit_date_estimation'}

        for field, req_field in req_fields.items():
            self.required_if(
                YES,
                field=field,
                field_required=req_field)

        self.validate_other_specify(field='clinic_visited')


class SymptomAssessmentFormValidator(FormValidator):

    def clean(self):

        self.required_if(
            YES,
            field='last_visit_date_estimated',
            field_required='last_visit_date_estimation')
