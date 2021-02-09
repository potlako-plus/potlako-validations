from edc_form_validators import FormValidator
from edc_constants.constants import NO


class PatientAvailabilityLogEntryFormValidator(FormValidator):

    def clean(self):

        self.required_if(
            NO,
            field='can_take_call',
            field_required='reason')

        self.validate_other_specify(field='reason')
