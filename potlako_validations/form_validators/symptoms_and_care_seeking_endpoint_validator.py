from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import YES
from edc_form_validators import FormValidator


class SymptomsAndCareSeekingEndpointFormValidator(FormValidator):
    codinator_exit_form_model = 'potlako_prn.coordinatorexit'

    codinator_exit_form_model_cls = django_apps.get_model(codinator_exit_form_model)

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

        self.validate_codinator_exit_required()

    def validate_codinator_exit_required(self):
        try:
            self.codinator_exit_form_model_cls.objects.get(
                subject_identifier=self.cleaned_data.get('subject_identifier'))
        except self.codinator_exit_form_model_cls.DoesNotExist:
            raise ValidationError('Coordinator exit form not completed. Please complete '
                                  'the coordinator exit form first.')
