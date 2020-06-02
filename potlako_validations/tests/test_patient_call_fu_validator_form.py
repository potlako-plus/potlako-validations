from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import NO, YES

from ..form_validators import PatientCallFuFormValidator
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

    def test_next_visit_delayed_no_count_none(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'next_visit_delayed': NO,
            'visit_delayed_count': None,
        }
        form_validator = PatientCallFuFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_next_visit_delayed_no_count_invalid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'next_visit_delayed': NO,
            'visit_delayed_count': 1,
        }
        form_validator = PatientCallFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('visit_delayed_count', form_validator._errors)

    def test_next_visit_delayed_yes_count_valid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'next_visit_delayed': YES,
            'visit_delayed_count': 1,
        }
        form_validator = PatientCallFuFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_next_visit_delayed_yes_count_none(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'next_visit_delayed': YES,
            'visit_delayed_count': None,
        }
        form_validator = PatientCallFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('visit_delayed_count', form_validator._errors)

    def test_next_visit_delayed_no_reason_none(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'next_visit_delayed': NO,
            'visit_delayed_reason': None,
        }
        form_validator = PatientCallFuFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_next_visit_delayed_no_reason_invalid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'next_visit_delayed': NO,
            'visit_delayed_reason': 'Reason',
        }
        form_validator = PatientCallFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('visit_delayed_reason', form_validator._errors)

    def test_next_visit_delayed_yes_reason_none(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'next_visit_delayed': YES,
            'visit_delayed_reason': None,
        }
        form_validator = PatientCallFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('visit_delayed_reason', form_validator._errors)

    def test_next_visit_delayed_yes_reason_valid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'next_visit_delayed': YES,
            'visit_delayed_reason': 'Reason',
        }
        form_validator = PatientCallFuFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
