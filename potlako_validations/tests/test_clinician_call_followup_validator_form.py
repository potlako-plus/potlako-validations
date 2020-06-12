from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import OTHER, YES, NOT_APPLICABLE

from ..form_validators import ClinicianCallFollowupFormValidator
from .models import SubjectConsent, SubjectVisit, Appointment


class TestClinicianCallFollowUpForm(TestCase):

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

        self.options = {
            'facility_visited': 'blah',
            'subject_visit': self.subject_visit,
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
            'subject_visit': self.subject_visit,
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
            'subject_visit': self.subject_visit,
            'patient_disposition': 'refer',
            'referral_date': get_utcnow(),
            'referral_facility': NOT_APPLICABLE,
            'referral_reason': 'blah',
            'referral_discussed': 'blah', }
        form_validator = ClinicianCallFollowupFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('referral_facility', form_validator._errors)

    def test_patient_disposition_referral_reason_invalid(self):
        self.options = {
            'subject_visit': self.subject_visit,
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
            'subject_visit': self.subject_visit,
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
            'subject_visit': self.subject_visit,
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
            'subject_visit': self.subject_visit,
            'patient_disposition': 'discharge',
            'return_visit_scheduled': 'blah',
            'return_visit_date': None}
        form_validator = ClinicianCallFollowupFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('return_visit_scheduled', form_validator._errors)

    def test_patient_disposition_discharge_date_invalid(self):
        self.options = {
            'subject_visit': self.subject_visit,
            'patient_disposition': 'discharge',
            'return_visit_scheduled': None,
            'return_visit_date': get_utcnow()}
        form_validator = ClinicianCallFollowupFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('return_visit_date', form_validator._errors)

    def test_patient_disposition_discharge_schedule_valid(self):
        self.options = {
            'subject_visit': self.subject_visit,
            'patient_disposition': 'discharge',
            'return_visit_scheduled': None,
            'return_visit_date': None}
        form_validator = ClinicianCallFollowupFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
