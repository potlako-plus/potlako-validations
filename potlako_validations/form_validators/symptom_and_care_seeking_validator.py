from edc_constants.constants import YES, NO, OTHER
from edc_form_validators import FormValidator


class SymptomAndCareSeekingFormValidator(FormValidator):

    def clean(self):

        self.m2m_other_specify(
            OTHER,
            m2m_field='symptoms_present',
            field_other='symptoms_present_other')

        fields_required = ['discussion_person', 'discussion_date',
                           'medical_advice', 'discussion_date_estimated']

        for field_required in fields_required:
            self.required_if(
                YES,
                field='symptoms_discussion',
                field_required=field_required)

        self.required_if(
            NO,
            field='symptoms_discussion',
            field_required='reason_no_discussion')

        self.validate_other_specify(field='reason_no_discussion')

        self.m2m_other_specify(
            OTHER,
            m2m_field='discussion_person',
            field_other='discussion_person_other')

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
