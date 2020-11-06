from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import OTHER, YES

from ..form_validators import InvestigationsOrderedFormValidator
from .models import SubjectConsent, SubjectVisit, Appointment
from .models import M2MModel, PathologyTestType

@tag('t1')
class TestInvestigationsOrderedForm(TestCase):

    def setUp(self):
        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111', consent_datetime=get_utcnow(),
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date())
        appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000')
        self.subject_visit = SubjectVisit.objects.create(
            appointment=appointment)

    def test_pathology_tests_ordered_type_invalid(self):
        PathologyTestType.objects.create(name='pathology',
                                         short_name='pathology')
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tests_ordered_type': PathologyTestType.objects.all(),
            'pathology_test': None,
            'pathology_test_other': None,
            'tests_ordered_type_other': None
        }
        form_validator = InvestigationsOrderedFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('pathology_test', form_validator._errors)
    
   
    def test_pathology_tests_ordered_type_valid(self):
        PathologyTestType.objects.create(name='pathology',
                                         short_name='pathology')
        M2MModel.objects.create(name='pathology',
                                     short_name='pathology')
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tests_ordered_type': PathologyTestType.objects.all(),
            'pathology_test': M2MModel.objects.all(),
            'pathology_test_other': None,
            'tests_ordered_type_other': None
        }
        form_validator = InvestigationsOrderedFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
    
    def test_imaging_tests_ordered_type_invalid(self):
        PathologyTestType.objects.create(name='blah',
                                         short_name='blah')
        PathologyTestType.objects.create(name='imaging',
                                         short_name='imaging')
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tests_ordered_type': PathologyTestType.objects.all(),
            'imaging_test_type': None,
        }
        form_validator = InvestigationsOrderedFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('imaging_test_type', form_validator._errors)
        
    def test_imaging_tests_ordered_type_valid(self):
        PathologyTestType.objects.create(name='blah',
                                         short_name='blah')
        PathologyTestType.objects.create(name='imaging',
                                         short_name='imaging')
        M2MModel.objects.create(name='blah',
                                     short_name='blah')
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tests_ordered_type': PathologyTestType.objects.all(),
            'imaging_test_type': M2MModel.objects.all(),
        }
        form_validator = InvestigationsOrderedFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
            
    def test_tests_ordered_date_estimated_invalid(self):
        PathologyTestType.objects.create(name='blah',
                                         short_name='blah')
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tests_ordered_type': PathologyTestType.objects.all(),
            'ordered_date': None,
            'ordered_date_estimated': YES,
        }
        form_validator = InvestigationsOrderedFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('ordered_date_estimated', form_validator._errors)
        
    def test_tests_ordered_date_estimated_valid1(self):
        PathologyTestType.objects.create(name='blah',
                                         short_name='blah')
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tests_ordered_type': PathologyTestType.objects.all(),
            'ordered_date': get_utcnow(),
            'ordered_date_estimated': YES,
            'ordered_date_estimation': 'here',
        }
        form_validator = InvestigationsOrderedFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
            
    def test_tests_ordered_date_estimated_valid2(self):
        PathologyTestType.objects.create(name='blah',
                                         short_name='blah')
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tests_ordered_type': PathologyTestType.objects.all(),
            'ordered_date': None,
            'ordered_date_estimated': None,
        }
        form_validator = InvestigationsOrderedFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
            
    def test_tests_ordered_date_estimation_invalid(self):
        PathologyTestType.objects.create(name='blah',
                                         short_name='blah')
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tests_ordered_type': PathologyTestType.objects.all(),
            'ordered_date': get_utcnow(),
            'ordered_date_estimated': YES,
            'ordered_date_estimation': None,
        }
        form_validator = InvestigationsOrderedFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('ordered_date_estimation', form_validator._errors)
        
    def test_tests_ordered_date_estimation_valid(self):
        PathologyTestType.objects.create(name='blah',
                                         short_name='blah')
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tests_ordered_type': PathologyTestType.objects.all(),
            'ordered_date': get_utcnow(),
            'ordered_date_estimated': YES,
            'ordered_date_estimation': 'here',
        }
        form_validator = InvestigationsOrderedFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
    
    def test_tests_ordered_type_other_valid(self):
        PathologyTestType.objects.create(name=OTHER,
                                         short_name=OTHER)
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tests_ordered_type': PathologyTestType.objects.all(),
        }
        form_validator = InvestigationsOrderedFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('tests_ordered_type_other', form_validator._errors)
    
    def test_tests_ordered_type_other_invalid(self):
        PathologyTestType.objects.create(name=OTHER,
                                         short_name=OTHER)
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tests_ordered_type': PathologyTestType.objects.all(),
            'tests_ordered_type_other': 'here',
        }
        form_validator = InvestigationsOrderedFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
    
    def test_pathology_tests_fna_location_invalid(self):
        PathologyTestType.objects.create(name='pathology',
                                         short_name='pathology')
        M2MModel.objects.create(name='FNA',
                                     short_name='FNA')
        
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tests_ordered_type': PathologyTestType.objects.all(),
            'pathology_test':  M2MModel.objects.all(),
        }
        form_validator = InvestigationsOrderedFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('fna_location', form_validator._errors)
    
   
    def test_pathology_tests_fna_location_valid(self):
        PathologyTestType.objects.create(name='pathology',
                                         short_name='pathology')
        M2MModel.objects.create(name='FNA',
                                     short_name='FNA')
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tests_ordered_type': PathologyTestType.objects.all(),
            'pathology_test':  M2MModel.objects.all(),
            'fna_location': 'arm'
        }
        form_validator = InvestigationsOrderedFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
            
    def test_pathology_tests_biopsy_location_invalid(self):
        PathologyTestType.objects.create(name='pathology',
                                         short_name='pathology')
        M2MModel.objects.create(name='biopsy',
                                     short_name='biopsy')
        
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tests_ordered_type': PathologyTestType.objects.all(),
            'pathology_test':  M2MModel.objects.all(),
        }
        form_validator = InvestigationsOrderedFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('biopsy_specify', form_validator._errors)
    
   
    def test_pathology_tests_biopsy_location_valid(self):
        PathologyTestType.objects.create(name='pathology',
                                         short_name='pathology')
        M2MModel.objects.create(name='biopsy',
                                     short_name='biopsy')
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tests_ordered_type': PathologyTestType.objects.all(),
            'pathology_test':  M2MModel.objects.all(),
            'biopsy_specify': 'arm'
        }
        form_validator = InvestigationsOrderedFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
    
    def test_pathology_tests_xray_location_invalid(self):
        PathologyTestType.objects.create(name='imaging',
                                         short_name='imaging')
        M2MModel.objects.create(name='xray',
                                     short_name='xray')
        
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tests_ordered_type': PathologyTestType.objects.all(),
            'imaging_test_type':  M2MModel.objects.all(),
        }
        form_validator = InvestigationsOrderedFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('xray_tests', form_validator._errors)
    
   
    def test_pathology_tests_xray_location_valid(self):
        PathologyTestType.objects.create(name='imaging',
                                         short_name='imaging')
        M2MModel.objects.create(name='xray',
                                     short_name='xray')
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tests_ordered_type': PathologyTestType.objects.all(),
            'imaging_test_type':  M2MModel.objects.all(),
            'xray_tests': 'arm'
        }
        form_validator = InvestigationsOrderedFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
    
    def test_pathology_tests_ultrasound_location_invalid(self):
        PathologyTestType.objects.create(name='imaging',
                                         short_name='imaging')
        M2MModel.objects.create(name='ultrasound',
                                     short_name='ultrasound')
        
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tests_ordered_type': PathologyTestType.objects.all(),
            'imaging_test_type':  M2MModel.objects.all(),
        }
        form_validator = InvestigationsOrderedFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('ultrasound_tests', form_validator._errors)
    
   
    def test_pathology_tests_ultrasound_location_valid(self):
        PathologyTestType.objects.create(name='imaging',
                                         short_name='imaging')
        M2MModel.objects.create(name='ultrasound',
                                     short_name='ultrasound')
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tests_ordered_type': PathologyTestType.objects.all(),
            'imaging_test_type':  M2MModel.objects.all(),
            'ultrasound_tests': 'arm'
        }
        form_validator = InvestigationsOrderedFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
            
    def test_pathology_tests_ct_invalid(self):
        PathologyTestType.objects.create(name='imaging',
                                         short_name='imaging')
        M2MModel.objects.create(name='CT',
                                     short_name='CT')
        
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tests_ordered_type': PathologyTestType.objects.all(),
            'imaging_test_type':  M2MModel.objects.all(),
        }
        form_validator = InvestigationsOrderedFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('ct_tests', form_validator._errors)
    
   
    def test_pathology_tests_ct_valid(self):
        PathologyTestType.objects.create(name='imaging',
                                         short_name='imaging')
        M2MModel.objects.create(name='CT',
                                     short_name='CT')
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tests_ordered_type': PathologyTestType.objects.all(),
            'imaging_test_type':  M2MModel.objects.all(),
            'ct_tests': 'arm'
        }
        form_validator = InvestigationsOrderedFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
    
    def test_pathology_tests_mri_invalid(self):
        PathologyTestType.objects.create(name='imaging',
                                         short_name='imaging')
        M2MModel.objects.create(name='MRI',
                                     short_name='MRI')
        
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tests_ordered_type': PathologyTestType.objects.all(),
            'imaging_test_type':  M2MModel.objects.all(),
        }
        form_validator = InvestigationsOrderedFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('mri_tests', form_validator._errors)
    
   
    def test_pathology_tests_mri_valid(self):
        PathologyTestType.objects.create(name='imaging',
                                         short_name='imaging')
        M2MModel.objects.create(name='MRI',
                                     short_name='MRI')
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tests_ordered_type': PathologyTestType.objects.all(),
            'imaging_test_type':  M2MModel.objects.all(),
            'mri_tests': 'arm'
        }
        form_validator = InvestigationsOrderedFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
            