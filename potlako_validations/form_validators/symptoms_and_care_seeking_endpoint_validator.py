from edc_constants.constants import YES

from edc_form_validators import FormValidator


class SymptomsAndCareSeekingEndpointFormValidator(FormValidator):

    def clean(self):

        fields_required = {
            'cancer_symptom_estimated': 'cancer_symptom_estimation',
            'discussion_date_estimated': 'discussion_date_estimation',
            'seek_help_date_estimated': 'seek_help_date_estimation',
            'first_seen_date_estimated': 'first_seen_date_estimation'}

        for field, field_required in fields_required.items():
            self.required_if(
                YES,
                field=field,
                field_required=field_required)
