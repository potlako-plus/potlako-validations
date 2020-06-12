from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import OTHER, NOT_APPLICABLE
from edc_constants.constants import YES

from ..form_validators import ClinicianCallEnrollmentFormValidator


class TestClinicianCallEnrollmentForm(TestCase):

    def setUp(self):

        self.options = {
            'screening_identifier': '1111111',
            'report_datetime': get_utcnow(),
            'call_clinician_type': 'blah',
            'facility_unit': 'blah',
            'kin_relationship': 'blah',
            'clinician_type': 'blah',
            'suspected_cancer': 'blah',
            'patient_disposition': 'blah',
            'investigated': 'blah',
            'national_identity': '77727777'
        }

    def test_form_valid(self):
        form_validator = ClinicianCallEnrollmentFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_call_clinician_type_other_invalid(self):

        self.options['call_clinician_type'] = OTHER
        form_validator = ClinicianCallEnrollmentFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('call_clinician_other', form_validator._errors)

    def test_call_clinician_type_other_valid(self):

        self.options['call_clinician_type'] = OTHER
        self.options['call_clinician_other'] = 'blah'
        form_validator = ClinicianCallEnrollmentFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_facility_unit_other_invalid(self):

        self.options['facility_unit'] = OTHER
        form_validator = ClinicianCallEnrollmentFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('unit_other', form_validator._errors)

    def test_faccility_unit_other_valid(self):

        self.options['facility_unit'] = OTHER
        self.options['unit_other'] = 'blah'
        form_validator = ClinicianCallEnrollmentFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_kin_relationship_other_invalid(self):

        self.options['kin_relationship'] = OTHER
        form_validator = ClinicianCallEnrollmentFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('kin_relation_other', form_validator._errors)

    def test_kin_relationship_other_valid(self):

        self.options['kin_relationship'] = OTHER
        self.options['kin_relation_other'] = 'blah'
        form_validator = ClinicianCallEnrollmentFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_clinician_type_other_invalid(self):

        self.options['clinician_type'] = OTHER
        form_validator = ClinicianCallEnrollmentFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('clinician_other', form_validator._errors)

    def test_clinician_type_other_valid(self):

        self.options['clinician_type'] = OTHER
        self.options['clinician_other'] = 'blah'
        form_validator = ClinicianCallEnrollmentFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_early_symptoms_date_invalid(self):

        self.options['early_symptoms_date_estimated'] = YES
        form_validator = ClinicianCallEnrollmentFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('early_symptoms_date_estimation', form_validator._errors)

    def test_early_symptoms_date_valid(self):

        self.options['early_symptoms_date_estimated'] = YES
        self.options['early_symptoms_date_estimation'] = 'blah'
        form_validator = ClinicianCallEnrollmentFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_referral_reason_invalid(self):

        self.options['patient_disposition'] = 'refer'
        self.options['referral_date'] = get_utcnow()
        self.options['referral_unit'] = 'blah'
        self.options['referral_facility'] = 'blah'
        self.options['referral_discussed'] = 'blah'
        self.options['clinician_designation'] = 'blah'
        self.options['referral_fu_date'] = get_utcnow()
        form_validator = ClinicianCallEnrollmentFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('referral_reason', form_validator._errors)

    def test_referral_date_invalid(self):

        self.options['patient_disposition'] = 'refer'
        self.options['referral_reason'] = 'blah'
        self.options['referral_unit'] = 'blah'
        self.options['referral_facility'] = 'blah'
        self.options['referral_discussed'] = 'blah'
        self.options['clinician_designation'] = 'blah'
        self.options['referral_fu_date'] = get_utcnow()
        form_validator = ClinicianCallEnrollmentFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('referral_date', form_validator._errors)

    def test_referral_unit_invalid(self):

        self.options['patient_disposition'] = 'refer'
        self.options['referral_date'] = get_utcnow()
        self.options['referral_reason'] = 'blah'
        self.options['referral_facility'] = 'blah'
        self.options['referral_discussed'] = 'blah'
        self.options['clinician_designation'] = 'blah'
        self.options['referral_unit'] = NOT_APPLICABLE
        self.options['referral_fu_date'] = get_utcnow()
        form_validator = ClinicianCallEnrollmentFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('referral_unit', form_validator._errors)

    def test_referral_discussed_invalid1(self):

        self.options['patient_disposition'] = 'refer'
        self.options['referral_date'] = get_utcnow()
        self.options['referral_reason'] = 'blah'
        self.options['referral_unit'] = 'blah'
        self.options['referral_facility'] = 'blah'
        self.options['clinician_designation'] = 'blah'
        self.options['referral_fu_date'] = get_utcnow()
        self.options['referral_discussed'] = NOT_APPLICABLE
        form_validator = ClinicianCallEnrollmentFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('referral_discussed', form_validator._errors)

    def test_referral_designation_invalid1(self):

        self.options['patient_disposition'] = 'refer'
        self.options['referral_date'] = get_utcnow()
        self.options['referral_reason'] = 'blah'
        self.options['referral_unit'] = 'blah'
        self.options['referral_facility'] = 'blah'
        self.options['referral_discussed'] = 'blah'
        self.options['referral_fu_date'] = get_utcnow()
        self.options['clinician_designation'] = NOT_APPLICABLE
        form_validator = ClinicianCallEnrollmentFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('clinician_designation', form_validator._errors)

    def test_referral_fu_date_invalid1(self):

        self.options['patient_disposition'] = 'refer'
        self.options['referral_date'] = get_utcnow()
        self.options['referral_reason'] = 'blah'
        self.options['referral_unit'] = 'blah'
        self.options['referral_facility'] = 'blah'
        self.options['referral_discussed'] = 'blah'
        self.options['clinician_designation'] = 'blah'
        form_validator = ClinicianCallEnrollmentFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('referral_fu_date', form_validator._errors)

    def test_referral_facility_invalid1(self):

        self.options['patient_disposition'] = 'refer'
        self.options['referral_date'] = get_utcnow()
        self.options['referral_reason'] = 'blah'
        self.options['referral_unit'] = 'blah'
        self.options['referral_discussed'] = 'blah'
        self.options['clinician_designation'] = 'blah'
        self.options['referral_fu_date'] = get_utcnow()
        form_validator = ClinicianCallEnrollmentFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('referral_facility', form_validator._errors)

    def test_referral_facility_invalid2(self):

        self.options['patient_disposition'] = 'refer'
        self.options['referral_reason'] = 'blah'
        self.options['referral_date'] = get_utcnow()
        self.options['referral_unit'] = 'blah'
        self.options['referral_facility'] = OTHER
        self.options['referral_discussed'] = 'blah'
        self.options['clinician_designation'] = 'blah'
        self.options['referral_fu_date'] = get_utcnow()
        form_validator = ClinicianCallEnrollmentFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('referral_facility_other', form_validator._errors)

    def test_referral_facility_valid(self):

        self.options['patient_disposition'] = 'refer'
        self.options['referral_reason'] = 'blah'
        self.options['referral_date'] = get_utcnow()
        self.options['referral_unit'] = 'blah'
        self.options['referral_facility'] = OTHER
        self.options['referral_discussed'] = 'blah'
        self.options['referral_fu_date'] = get_utcnow()
        self.options['referral_facility_other'] = 'blah'
        form_validator = ClinicianCallEnrollmentFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_investigation_notes_invalid(self):

        self.options['investigated'] = YES
        self.options['investigation_notes'] = NOT_APPLICABLE
        form_validator = ClinicianCallEnrollmentFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('investigation_notes', form_validator._errors)

    def test_investigation_notes_valid(self):

        self.options['investigated'] = YES
        self.options['investigation_notes'] = 'blah'
        form_validator = ClinicianCallEnrollmentFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
