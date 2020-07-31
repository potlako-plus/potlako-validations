from edc_form_validators import FormValidator
from .crf_form_validator import CRFFormValidator


class InvestigationsResultedFormValidator(CRFFormValidator, FormValidator):

    def clean(self):

        self.subject_identifier = self.cleaned_data.get(
            'subject_visit').appointment.subject_identifier

        super().clean()
