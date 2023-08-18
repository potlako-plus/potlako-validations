from django.core.exceptions import ValidationError
from django.test import tag, TestCase
from model_mommy import mommy

from potlako_validations.form_validators import CancerDxAndTxEndpointFormValidator
from potlako_validations.tests.models import CancerDxAndTxEndpoint, \
    SymptomsAndCareSeekingEndpoint


@tag('cancer_dx_and_tx_endpoint')
class TestCancerDxAndTxEndpointValidator(TestCase):

    def setUp(self):
        care_seeking_endpoint_model = 'potlako_validations.symptomsandcareseekingendpoint'
        CancerDxAndTxEndpointFormValidator.care_seeking_endpoint_model = \
            care_seeking_endpoint_model

    def test_validate_care_seeking_endpoint_completed_not_raised(self):
        care_seeking_endpoint = mommy.make(CancerDxAndTxEndpoint)
        cleaned_data = {
            'subject_identifier': care_seeking_endpoint.subject_identifier
        }

        form_validator = CancerDxAndTxEndpointFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(
                f"validate_care_seeking_endpoint_completed raised ValidationError "
                f"unexpectedly: {e}")

    def test_validate_care_seeking_endpoint_completed_raised(self):
        cleaned_data = {
            'subject_identifier': '332312'
        }

        form_validator = CancerDxAndTxEndpointFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('final_deposition', form_validator._errors)
