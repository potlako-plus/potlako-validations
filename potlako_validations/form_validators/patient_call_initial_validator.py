from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import NO, OTHER, YES, POS
from edc_form_validators import FormValidator

from .crf_form_validator import CRFFormValidator


class PatientCallInitialFormValidator(CRFFormValidator, FormValidator):

    def clean(self):
        
        self.subject_identifier = self.cleaned_data.get(
            'subject_visit').appointment.subject_identifier
            
        self.required_if(
            YES,
            field='work_status',
            field_required='work_type',)

        self.required_if(
            YES,
            field='potlako_sms_received',
            field_required='sms_platform',)

        self.required_if(
            NO,
            field='work_status',
            field_required='unemployed_reason',)

        self.not_required_if(
            NO,
            field='other_facility',
            field_required='facility_number',)

        other_fields = ['primary_clinic', 'work_type',
                        'residential_district', 'unemployed_reason',
                        'enrollment_visit_method', 'next_ap_facility',
                        'next_ap_facility_unit']

        for other_field in other_fields:
            self.validate_other_specify(
                other_field)

        self.required_if(
            YES,
            field='heard_of_potlako',
            field_required='source_of_info')

        self.m2m_required_if(
            YES,
            field='potlako_sms_received',
            m2m_field='sms_platform')
        
        self.m2m_other_specify(
            OTHER,
            m2m_field='source_of_info',
            field_other='source_of_info_other')

        self.m2m_other_specify(
            OTHER,
            m2m_field='sms_platform',
            field_other='sms_platform_other')

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
        
        self.required_if(
            POS,
            field='hiv_status',
            field_required='cd4_count',)
        
        self.required_if(
            POS,
            field='hiv_status',
            field_required='vl_results',)
        
        self.validate_next_appointment_date(
            next_ap_date=self.cleaned_data.get('next_appointment_date'))
        
        super().clean()

