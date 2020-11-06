from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import NO, OTHER, YES

from ..form_validators import InvestigationsFormValidator
from .models import SubjectConsent, SubjectVisit, Appointment


class TestPatientCallFuForm(TestCase):

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

    def test_lab_tests_ordered_none(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'lab_tests_ordered': NO,
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_lab_tests_ordered_date_invalid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'lab_tests_ordered': YES,
            'facility_ordered': 'blah',
            'ordered_date': None,
            'ordered_date_estimated': NO
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('ordered_date', form_validator._errors)

    def test_lab_tests_ordered_facility_invalid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'lab_tests_ordered': YES,
            'facility_ordered': None,
            'ordered_date': get_utcnow(),
            'ordered_date_estimated': NO
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('facility_ordered', form_validator._errors)

    def test_lab_tests_ordered_estimated_invalid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'lab_tests_ordered': YES,
            'facility_ordered': 'blah',
            'ordered_date': get_utcnow(),
            'ordered_date_estimated': None
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('ordered_date_estimated', form_validator._errors)

    def test_lab_tests_ordered_estimated_valid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'lab_tests_ordered': YES,
            'facility_ordered': 'blah',
            'ordered_date': get_utcnow(),
            'ordered_date_estimated': YES,
            'ordered_date_estimation': 'blah'
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_lab_tests_ordered_estimation_invalid1(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'lab_tests_ordered': YES,
            'facility_ordered': 'blah',
            'ordered_date': get_utcnow(),
            'ordered_date_estimated': NO,
            'ordered_date_estimation': 'blah'
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('ordered_date_estimation', form_validator._errors)

    def test_lab_tests_ordered_estimation_invalid2(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'lab_tests_ordered': YES,
            'facility_ordered': 'balh',
            'ordered_date': get_utcnow(),
            'ordered_date_estimated': YES,
            'ordered_date_estimation': None
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('ordered_date_estimation', form_validator._errors)

    def test_pathology_tests_ordered_none(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'pathology_tests_ordered': NO,
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_pathology_tests_ordered_invalid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'pathology_tests_ordered': YES,
            'pathology_test': None,
            'pathology_specimen_date': get_utcnow(),
            'pathology_nhl_date': get_utcnow(),
            'pathology_result_date': get_utcnow(),
            'pathology_received_date': get_utcnow(),
            'pathology_communicated_date': get_utcnow(),
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('pathology_test', form_validator._errors)

    def test_pathology_specimen_date_invalid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'pathology_tests_ordered': YES,
            'pathology_test': 'blah',
            'pathology_specimen_date': None,
            'pathology_nhl_date': get_utcnow(),
            'pathology_result_date': get_utcnow(),
            'pathology_received_date': get_utcnow(),
            'pathology_communicated_date': get_utcnow(),
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('pathology_specimen_date', form_validator._errors)

    def test_pathology_nhl_date_invalid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'pathology_tests_ordered': YES,
            'pathology_test': 'blah',
            'pathology_specimen_date': get_utcnow(),
            'pathology_nhl_date': None,
            'pathology_result_date': get_utcnow(),
            'pathology_received_date': get_utcnow(),
            'pathology_communicated_date': get_utcnow(),
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('pathology_nhl_date', form_validator._errors)

    def test_pathology_result_date_invalid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'pathology_tests_ordered': YES,
            'pathology_test': 'blah',
            'pathology_specimen_date': get_utcnow(),
            'pathology_nhl_date': get_utcnow(),
            'pathology_result_date': None,
            'pathology_received_date': get_utcnow(),
            'pathology_communicated_date': get_utcnow(),
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('pathology_result_date', form_validator._errors)

    def test_pathology_recieved_date_invalid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'pathology_tests_ordered': YES,
            'pathology_test': 'blah',
            'pathology_specimen_date': get_utcnow(),
            'pathology_nhl_date': get_utcnow(),
            'pathology_result_date': get_utcnow(),
            'pathology_received_date': None,
            'pathology_communicated_date': get_utcnow(),
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('pathology_received_date', form_validator._errors)

    def test_pathology_communicated_date_invalid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'pathology_tests_ordered': YES,
            'pathology_test': 'blah',
            'pathology_specimen_date': get_utcnow(),
            'pathology_nhl_date': get_utcnow(),
            'pathology_result_date': get_utcnow(),
            'pathology_received_date': get_utcnow(),
            'pathology_communicated_date': None,
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('pathology_communicated_date', form_validator._errors)

    def test_pathology_test_fna_valid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'pathology_tests_ordered': YES,
            'pathology_test': 'FNA',
            'fna_location': 'blah',
            'pathology_specimen_date': get_utcnow(),
            'pathology_nhl_date': get_utcnow(),
            'pathology_result_date': get_utcnow(),
            'pathology_received_date': get_utcnow(),
            'pathology_communicated_date': get_utcnow(),
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_pathology_test_fna_invalid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'pathology_tests_ordered': YES,
            'pathology_test': 'FNA',
            'fna_location': None,
            'pathology_specimen_date': get_utcnow(),
            'pathology_nhl_date': get_utcnow(),
            'pathology_result_date': get_utcnow(),
            'pathology_received_date': get_utcnow(),
            'pathology_communicated_date': get_utcnow(),
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('fna_location', form_validator._errors)

    def test_pathology_test_biopsy_valid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'pathology_tests_ordered': YES,
            'pathology_test': 'biopsy_other',
            'biopsy_other': 'blah',
            'pathology_specimen_date': get_utcnow(),
            'pathology_nhl_date': get_utcnow(),
            'pathology_result_date': get_utcnow(),
            'pathology_received_date': get_utcnow(),
            'pathology_communicated_date': get_utcnow(),
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_pathology_test_biopsy_invalid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'pathology_tests_ordered': YES,
            'pathology_test': 'biopsy_other',
            'biopsy_other': None,
            'pathology_specimen_date': get_utcnow(),
            'pathology_nhl_date': get_utcnow(),
            'pathology_result_date': get_utcnow(),
            'pathology_received_date': get_utcnow(),
            'pathology_communicated_date': get_utcnow(),
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('biopsy_other', form_validator._errors)

    def test_imaging_test_none(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'imaging_tests': NO,
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_imaging_test_status_invalid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'imaging_tests': YES,
            'imaging_test_status': None,
            'imaging_test_type': 'blah',
            'imaging_tests_date': get_utcnow(),
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('imaging_test_status', form_validator._errors)

    def test_imaging_test_type_invalid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'imaging_tests': YES,
            'imaging_test_status': 'biopsy_other',
            'imaging_test_type': None,
            'imaging_tests_date': get_utcnow(),
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('imaging_test_type', form_validator._errors)

    def test_imaging_tests_date_invalid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'imaging_tests': YES,
            'imaging_test_status': 'biopsy_other',
            'imaging_test_type': 'blah',
            'imaging_tests_date': None,
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('imaging_tests_date', form_validator._errors)

    def test_imaging_test_ultrasoud_valid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'imaging_tests': YES,
            'imaging_test_status': 'biopsy_other',
            'imaging_test_type': 'ultrasound_other',
            'imaging_tests_date': get_utcnow(),
            'ultrasound_tests': 'blah'
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_imaging_test_ultrasoud_invalid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'imaging_tests': YES,
            'imaging_test_status': 'biopsy_other',
            'imaging_test_type': 'ultrasound_other',
            'imaging_tests_date': get_utcnow(),
            'ultrasound_tests': None
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('ultrasound_tests', form_validator._errors)

    def test_imaging_test_ct_valid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'imaging_tests': YES,
            'imaging_test_status': 'biopsy_other',
            'imaging_test_type': 'CT',
            'imaging_tests_date': get_utcnow(),
            'ct_tests': 'blah'
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_imaging_test_ct_invalid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'imaging_tests': YES,
            'imaging_test_status': 'biopsy_other',
            'imaging_test_type': 'CT',
            'imaging_tests_date': get_utcnow(),
            'ct_tests': None
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('ct_tests', form_validator._errors)

    def test_imaging_test_mri_valid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'imaging_tests': YES,
            'imaging_test_status': 'biopsy_other',
            'imaging_test_type': 'MRI',
            'imaging_tests_date': get_utcnow(),
            'mri_tests': 'blah'
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_imaging_test_mri_invalid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'imaging_tests': YES,
            'imaging_test_status': 'biopsy_other',
            'imaging_test_type': 'MRI',
            'imaging_tests_date': get_utcnow(),
            'mri_tests': None
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('mri_tests', form_validator._errors)

    def test_facility_ordered_other_valid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'lab_tests_ordered': YES,
            'facility_ordered': OTHER,
            'ordered_date': get_utcnow(),
            'ordered_date_estimated': NO,
            'facility_ordered_other': 'blah'
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_facility_ordered_other_invalid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'lab_tests_ordered': YES,
            'facility_ordered': OTHER,
            'ordered_date': get_utcnow(),
            'ordered_date_estimated': NO,
            'facility_ordered_other': None
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('facility_ordered_other', form_validator._errors)

    def test_imaging_tests_other_valid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'imaging_tests': YES,
            'imaging_test_status': 'biopsy_other',
            'imaging_test_type': OTHER,
            'imaging_tests_date': get_utcnow(),
            'imaging_test_type_other': 'blah'
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_imaging_tests_other_invalid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'imaging_tests': YES,
            'imaging_test_status': 'biopsy_other',
            'imaging_test_type': OTHER,
            'imaging_tests_date': get_utcnow(),
            'imaging_test_type_other': None
        }
        form_validator = InvestigationsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('imaging_test_type_other', form_validator._errors)
