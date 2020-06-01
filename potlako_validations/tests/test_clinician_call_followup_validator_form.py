from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import OTHER, NOT_APPLICABLE
from edc_constants.constants import YES, NO

from ..form_validators import ClinicianCallFollowupFormValidator


@tag('cfu')
class TestClinicianCallFollowUpForm(TestCase):

    def setUp(self):

        self.options = {
            'facility_visited': 'blah',
        }

    def test_form_valid(self):
        form_validator = ClinicianCallFollowupFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_facility_visited_other_invalid(self):

        self.options['facility_visited'] = OTHER
        form_validator = ClinicianCallFollowupFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('facility_visited_other', form_validator._errors)

    def test_facility_visited_other_valid(self):

        self.options['facility_visited'] = OTHER
        self.options['facility_visited_other'] = 'blah'
        form_validator = ClinicianCallFollowupFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_facility_unit_other_invalid(self):

        self.options['facility_unit'] = OTHER
        form_validator = ClinicianCallFollowupFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('facility_unit_other', form_validator._errors)

    def test_facility_unit_other_valid(self):

        self.options['facility_unit'] = OTHER
        self.options['facility_unit_other'] = 'blah'
        form_validator = ClinicianCallFollowupFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_patient_disposition_referral_date_invalid(self):
        self.options = {
            'patient_disposition': 'refer',
            'referral_date': None,
            'referral_facility': 'blah',
            'referral_reason': 'blah',
            'referral_discussed': 'blah', }
        form_validator = ClinicianCallFollowupFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('referral_date', form_validator._errors)

    def test_patient_disposition_referral_facility_invalid(self):
        self.options = {
            'patient_disposition': 'refer',
            'referral_date': get_utcnow(),
            'referral_facility': None,
            'referral_reason': 'blah',
            'referral_discussed': 'blah', }
        form_validator = ClinicianCallFollowupFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('referral_facility', form_validator._errors)

    def test_patient_disposition_referral_reason_invalid(self):
        self.options = {
            'patient_disposition': 'refer',
            'referral_date': get_utcnow(),
            'referral_facility': 'blah',
            'referral_reason': None,
            'referral_discussed': 'blah', }
        form_validator = ClinicianCallFollowupFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('referral_reason', form_validator._errors)

    def test_patient_disposition_referral_discussed_invalid(self):
        self.options = {
            'patient_disposition': 'refer',
            'referral_date': get_utcnow(),
            'referral_facility': 'blah',
            'referral_reason': 'blah',
            'referral_discussed': None, }
        form_validator = ClinicianCallFollowupFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('referral_discussed', form_validator._errors)

    def test_referral_discussed_clinician_invalid(self):
        self.options = {
            'patient_disposition': 'refer',
            'referral_date': get_utcnow(),
            'referral_facility': 'blah',
            'referral_reason': 'blah',
            'referral_discussed': YES,
            'referral_discussed_clinician': None}
        form_validator = ClinicianCallFollowupFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('referral_discussed_clinician', form_validator._errors)

    def test_patient_disposition_discharge_schedule_invalid(self):
        self.options = {
            'patient_disposition': 'discharge',
            'return_visit_scheduled': 'blah',
            'return_visit_date': None}
        form_validator = ClinicianCallFollowupFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('return_visit_scheduled', form_validator._errors)

    def test_patient_disposition_discharge_date_invalid(self):
        self.options = {
            'patient_disposition': 'discharge',
            'return_visit_scheduled': None,
            'return_visit_date': get_utcnow()}
        form_validator = ClinicianCallFollowupFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('return_visit_date', form_validator._errors)

    def test_patient_disposition_discharge_schedule_valid(self):
        self.options = {
            'patient_disposition': 'discharge',
            'return_visit_scheduled': None,
            'return_visit_date': None}
        form_validator = ClinicianCallFollowupFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
