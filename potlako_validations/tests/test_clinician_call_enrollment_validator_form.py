from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO

from ..form_validators import ClinicianCallEnrollmentFormValidator


class TestClinicianCallEnrollmentForm(TestCase):

    def setUp(self):
        ClinicianCallEnrollmentFormValidator.clinician_call_enrollment_model = \
            'potlako_validations.cliniciancallenrollment'
        ClinicianCallEnrollmentFormValidator.subject_consent_model = \
            'potlako_validations.subjectconsent'
        ClinicianCallEnrollmentFormValidator.subject_screening_model = \
            'potlako_validations.subjectscreening'

    def test_form_valid(self):
        cleaned_data = {
            'screening_identifier': '1111111',
            'report_datetime': get_utcnow(),
            'call_clinician_type': 'blah',
            'facility_unit': 'blah',
            'kin_relationship': 'blah',
            'clinician_type': 'blah',
            'symptoms': 'blah',
            'early_symptoms_date_estimated': NO,
            'suspected_cancer': 'blah',
            'patient_disposition': 'blah',
            'investigated': 'blah'
        }
        form_validator = ClinicianCallEnrollmentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

