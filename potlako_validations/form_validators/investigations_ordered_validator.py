from edc_constants.constants import YES, OTHER
from edc_form_validators import FormValidator
from .crf_form_validator import CRFFormValidator


class InvestigationsOrderedFormValidator(CRFFormValidator, FormValidator):
    
    def clean(self):

        self.subject_identifier = self.cleaned_data.get(
            'subject_visit').appointment.subject_identifier

        self.m2m_other_specify(
            'pathology',
            m2m_field='tests_ordered_type',
            field_other='pathology_test')
        
        self.m2m_other_specify(
            'imaging',
            m2m_field='tests_ordered_type',
            field_other='imaging_test_type')

        self.m2m_other_specify(
            'imaging',
            m2m_field='tests_ordered_type',
            field_other='imaging_test_status')
        
        self.required_if_not_none(
            field='ordered_date',
            field_required='ordered_date_estimated')

        self.required_if(
            YES,
            field='ordered_date_estimated',
            field_required='ordered_date_estimation')

        self.m2m_other_specify(
            OTHER,
            m2m_field='tests_ordered_type',
            field_other='tests_ordered_type_other')
        
        self.m2m_other_specify(
            'FNA',
            m2m_field='pathology_test',
            field_other='fna_location')
        
        self.m2m_other_specify(
            'biopsy',
            m2m_field='pathology_test',
            field_other='biopsy_specify')
        
        self.m2m_other_specify(
            'xray',
            m2m_field='imaging_test_type',
            field_other='xray_tests')
        
        self.m2m_other_specify(
            'ultrasound',
            m2m_field='imaging_test_type',
            field_other='ultrasound_tests')
        
        self.m2m_other_specify(
            'CT',
            m2m_field='imaging_test_type',
            field_other='ct_tests')
        
        self.m2m_other_specify(
            'MRI',
            m2m_field='imaging_test_type',
            field_other='mri_tests')

        self.m2m_other_specify(
            OTHER,
            m2m_field='pathology_test',
            field_other='pathology_test_other')

        self.m2m_other_specify(
            OTHER,
            m2m_field='imaging_test_type',
            field_other='imaging_test_type_other')

        self.validate_other_specify(
            'facility_ordered')

        super().clean()
