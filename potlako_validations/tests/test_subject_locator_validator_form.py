from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from django.utils import timezone
from edc_constants.constants import YES, NO

from ..form_validators import SubjectLocatorFormValidator

@tag('2')
class TestSubjectLocatorForm(TestCase):

    def setUp(self):

        self.options = {
            'screening_identifier': '1111111',
            'report_datetime': timezone.now,
            'local_clinic': 'blah',
            'home_village': 'blah',
            'has_alt_contact': YES,
            'alt_contact_name': 'blah',
            'alt_contact_rel': 'blah',
            'alt_contact_cell': '74564233',
            'alt_contact_tel': '3569674',
        }

    def test_form_valid(self):
        form_validator = SubjectLocatorFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_next_of_kin_has_cell(self):
        form_validator = SubjectLocatorFormValidator(
            cleaned_data=self.options)
        self.options['alt_contact_cell'] = None
        try:
            form_validator.validate()
        except  ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_next_of_kin_has_tel(self):
        form_validator = SubjectLocatorFormValidator(
            cleaned_data=self.options)
        self.options['alt_contact_tel'] = None
        try:
            form_validator.validate()
        except  ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_has_alt_contact(self):
        form_validator = SubjectLocatorFormValidator(
            cleaned_data=self.options)
        self.options['has_alt_contact'] = NO
        self.options['alt_contact_name'] = None
        self.options['alt_contact_rel'] = None
        self.options['alt_contact_cell'] = None
        self.options['alt_contact_tel'] = None

        try:
            form_validator.validate()
        except  ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
