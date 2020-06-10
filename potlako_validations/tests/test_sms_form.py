from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow

from ..form_validators import SmsFormValidator


@tag('sms')
class TestSmsForm(TestCase):

    def test_date_reminder_sent_invalid(self):
        cleaned_data = {
            'next_ap_date': get_utcnow().date() + relativedelta(days=1),
            'date_reminder_sent': get_utcnow().date() - relativedelta(days=1)
        }
        form_validator = SmsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('date_reminder_sent', form_validator._errors)

    def test_date_reminder_sent_valid(self):
        cleaned_data = {
            'next_ap_date': get_utcnow().date() + relativedelta(days=1),
            'date_reminder_sent': get_utcnow().date()
        }
        form_validator = SmsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
