from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator


class SmsFormValidator(FormValidator):

    def clean(self):

        next_ap_date = self.cleaned_data.get('next_ap_date')

        date_reminder_sent = self.cleaned_data.get('date_reminder_sent')

        expected_date = next_ap_date - relativedelta(days=1)

        if (date_reminder_sent != expected_date):
            msg = {'date_reminder_sent': 'Date reminder sent must be a day '
                   f'before the next appointment date. Got  {date_reminder_sent}'
                   f' expected {expected_date}'}
            self._errors.update(msg)
            raise ValidationError(msg)
