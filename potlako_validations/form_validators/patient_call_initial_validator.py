
from edc_constants.constants import NO, OTHER, YES
from edc_form_validators import FormValidator


class PatientCallInitialFormValidator(FormValidator):

    def clean(self):
        self.required_if(
            YES,
            field='work_status',
            field_required='work_type',)

        self.required_if(
            NO,
            field='work_status',
            field_required='unemployed_reason',)

        self.required_if(
            YES,
            field='patient_symptoms_date_estimated',
            field_required='patient_symptoms_date_estimation',)

        self.not_required_if(
            0,
            field='symptoms_duration_report',
            field_required='symptoms_duration',)

        self.not_required_if(
            NO,
            field='other_facility',
            field_required='facility_number',)

        other_fields = ['primary_clinic', 'work_type', 'residential_district',
                        'unemployed_reason', 'enrollment_visit_method',
                        'next_ap_facility', 'next_ap_facility_unit']

        for other_field in other_fields:
            self.validate_other_specify(
                other_field)

        self.m2m_other_specify(
            OTHER,
            m2m_field='patient_residence',
            field_other='patient_residence_other')

        self.m2m_other_specify(
            OTHER,
            m2m_field='call_achievements',
            field_other='call_achievements_other')

        self.required_if_not_none(
            field='hiv_test_date',
            field_required='hiv_test_date_estimated',)

        self.required_if(
            YES,
            field='hiv_test_date_estimated',
            field_required='hiv_test_date_estimation',)
