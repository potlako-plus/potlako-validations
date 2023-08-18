from django.core.exceptions import ValidationError
from django.test import tag, TestCase
from model_mommy import mommy

from potlako_validations.form_validators import \
    SymptomsAndCareSeekingEndpointFormValidator
from potlako_validations.tests.models import SymptomsAndCareSeekingEndpoint


class TestSymptomsAndCareSeekingEndpointFormValidator(TestCase):
    def setUp(self):
        codinator_exit_form_model = 'potlako_validations.symptomsandcareseekingendpoint'
        SymptomsAndCareSeekingEndpointFormValidator.care_seeking_endpoint_model = \
            codinator_exit_form_model

    def test_validate_symptoms_and_care_seeking_endpoint_completed_not_raised(self):
        codinator_exit = mommy.make(SymptomsAndCareSeekingEndpoint)
        cleaned_data = {
            'subject_identifier': codinator_exit.subject_identifier
        }

        form_validator = SymptomsAndCareSeekingEndpointFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(
                f"validate_care_seeking_endpoint_completed raised ValidationError "
                f"unexpectedly: {e}")

    def test_validate_symptoms_and_care_seeking_endpoint_completed_raised(self):
        cleaned_data = {
            'subject_identifier': '332312'
        }

        form_validator = SymptomsAndCareSeekingEndpointFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('final_deposition', form_validator._errors)