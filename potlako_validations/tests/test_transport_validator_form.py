from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import NO, YES

from potlako_subject.models.list_models import TransportCriteria

from ..form_validators import TransportFormValidator


@tag('trans')
class TestSmsorm(TestCase):

    def setUp(self):
        TransportCriteria.objects.create(
            name='disability',
            short_name='Unable to work due to physical or mental disability')

    def test_criteria_met_yes_trans_type_required(self):
        cleaned_data = {
            'is_criteria_met': YES,
            'transport_type': None}

        form_validator = TransportFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('transport_type', form_validator._errors)

    def test_criteria_met_no_trans_type_invalid(self):
        cleaned_data = {
            'is_criteria_met': NO,
            'transport_type': 'bus'}
        form_validator = TransportFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('transport_type', form_validator._errors)

    def test_criteria_met_yes_trans_type_valid(self):
        cleaned_data = {
            'is_criteria_met': YES,
            'criteria_met': TransportCriteria.objects.filter(name='disability'),
            'transport_type': 'bus'}
        form_validator = TransportFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_criteria_met_no_trans_type_valid(self):
        cleaned_data = {
            'is_criteria_met': NO,
            'transport_type': None}
        form_validator = TransportFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
