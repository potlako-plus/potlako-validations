from edc_form_validators import FormValidator


class BaselineClinicalSummaryFormValidator(FormValidator):

    def clean(self):

        self.validate_other_specify(field='cancer_concern')
