from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import NO, YES

from ..form_validators import MissedVisitFormValidator
from .models import SubjectConsent, SubjectVisit, Appointment


class TestMissedVisittForm(TestCase):

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

    def test_not_inquired_reason_valid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'inquired': NO,
            'not_inquired_reason': 'blah',
        }
        form_validator = MissedVisitFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_not_inquired_reason_invalid1(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'inquired': NO,
            'not_inquired_reason': None,
        }
        form_validator = MissedVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('not_inquired_reason', form_validator._errors)

    def test_not_inquired_reason_invalid2(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'inquired': YES,
            'not_inquired_reason': 'blah',
            'inquired_from': 'blah'
        }
        form_validator = MissedVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('not_inquired_reason', form_validator._errors)

    def test_transport_support_need_valid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'transport_support': NO,
            'transport_need': YES,
        }
        form_validator = MissedVisitFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_transport_support_need_invalid1(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'transport_support': NO,
            'transport_need': None,
        }
        form_validator = MissedVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('transport_need', form_validator._errors)

    def test_transport_support_need_invalid2(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'transport_support': YES,
            'transport_need': 'blah',
        }
        form_validator = MissedVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('transport_need', form_validator._errors)

    def test_inquired_from_valid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'inquired': YES,
            'inquired_from': 'blah',
        }
        form_validator = MissedVisitFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_inquired_from_invalid1(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'inquired': NO,
            'not_inquired_reason': 'blah',
            'inquired_from': 'blah',
        }
        form_validator = MissedVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('inquired_from', form_validator._errors)

    def test_inquired_from_invalid2(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'inquired': YES,
            'inquired_from': None,
        }
        form_validator = MissedVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('inquired_from', form_validator._errors)
