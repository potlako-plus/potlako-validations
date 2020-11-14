from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import OTHER

from ..form_validators import BaselineClinicalSummaryFormValidator


class TestBaselineClinicalSummaryForm(TestCase):

    def setUp(self):

        self.options = {
            'subject_identifier': '12345',
            'report_datetime': get_utcnow(),
            'symptoms_summary': 'blah blah',
            'cancer_concern': 'breast',
            'cancer_concern_other': None,
            'cancer_probability': 'low',
        }

    def test_form_valid(self):
        """
        Checks form saves successfully with all necessary field
        values completed.
        """
        form_validator = BaselineClinicalSummaryFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_cancer_concern_other_invalid(self):
        """
        Assert raises validation error if cancer concern other is
        selected, but cancer concern other is not specified.
        """
        self.options['cancer_concern'] = OTHER
        form_validator = BaselineClinicalSummaryFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('cancer_concern_other', form_validator._errors)

    def test_cancer_concern_other_valid(self):
        """
        Checks that no validation error raised if cancer concern other is
        selected, and cancer concern other is specified.
        """
        self.options['cancer_concern'] = OTHER
        self.options['cancer_concern_other'] = 'blah'
        form_validator = BaselineClinicalSummaryFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
