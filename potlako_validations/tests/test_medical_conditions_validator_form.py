from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_constants.constants import NO, OTHER, YES

from ..form_validators import MedicalConditionsFormValidator


@tag('mc')
class TestMedicalConditionsForm(TestCase):

    def test_diagnosis_date_estimate_no(self):
        cleaned_data = {
            'diagnosis_date_estimate': NO,
            'on_medicationon_medication': NO,
            'medical_condition': 'blah'
        }
        form_validator = MedicalConditionsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_diagnosis_date_estimate_invalid1(self):
        cleaned_data = {
            'diagnosis_date_estimate': YES,
            'diagnosis_date_estimation': None,
            'on_medicationon_medication': NO,
            'medical_condition': 'blah'
        }
        form_validator = MedicalConditionsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('diagnosis_date_estimation', form_validator._errors)

    def test_treatment_type_invalid(self):
        cleaned_data = {
            'diagnosis_date_estimate': YES,
            'diagnosis_date_estimation': 'blah',
            'on_medication': YES,
            'treatment_type': None,
            'medical_condition': 'blah'
        }
        form_validator = MedicalConditionsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('treatment_type', form_validator._errors)

    def test_treatment_name_invalid(self):
        cleaned_data = {
            'diagnosis_date_estimate': YES,
            'diagnosis_date_estimation': 'blah',
            'on_medication': YES,
            'treatment_type': 'blah',
            'treatment_name': None,
            'medical_condition': 'blah'
        }
        form_validator = MedicalConditionsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('treatment_name', form_validator._errors)

    def test_medical_condition_other_invalid(self):
        cleaned_data = {
            'diagnosis_date_estimate': YES,
            'diagnosis_date_estimation': 'blah',
            'on_medication': YES,
            'treatment_type': 'blah',
            'treatment_name': 'blah',
            'medical_condition': OTHER,
            'medical_condition_other': None
        }
        form_validator = MedicalConditionsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('medical_condition_other', form_validator._errors)

    def test_medical_condition_other_valid(self):
        cleaned_data = {
            'diagnosis_date_estimate': YES,
            'diagnosis_date_estimation': 'blah',
            'on_medication': YES,
            'treatment_type': 'blah',
            'treatment_name': 'blah',
            'medical_condition': OTHER,
            'medical_condition_other': 'blah'
        }
        form_validator = MedicalConditionsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

