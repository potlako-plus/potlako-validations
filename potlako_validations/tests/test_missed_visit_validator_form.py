from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_constants.constants import NO, YES

from ..form_validators import MissedVisitFormValidator


@tag('mv')
class TestMissedVisittForm(TestCase):

    def test_not_inquired_reason_valid(self):
        cleaned_data = {
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
            'inquired': NO,
            'not_inquired_reason': None,
        }
        form_validator = MissedVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('not_inquired_reason', form_validator._errors)

    def test_not_inquired_reason_invalid2(self):
        cleaned_data = {
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
            'transport_support': NO,
            'transport_need': None,
        }
        form_validator = MissedVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('transport_need', form_validator._errors)

    def test_transport_support_need_invalid2(self):
        cleaned_data = {
            'transport_support': YES,
            'transport_need': 'blah',
        }
        form_validator = MissedVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('transport_need', form_validator._errors)

    def test_inquired_from_valid(self):
        cleaned_data = {
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
            'inquired': YES,
            'inquired_from': None,
        }
        form_validator = MissedVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('inquired_from', form_validator._errors)
