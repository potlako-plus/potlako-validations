from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import ALIVE, OTHER

from ..form_validators import HomeVisitFormValidator
from .models import SubjectConsent, SubjectVisit, Appointment


class TestPatientCallFuForm(TestCase):

    def setUp(self):
        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111', consent_datetime=get_utcnow(),
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date())
        appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000')
        self.subject_visit = SubjectVisit.objects.create(
            appointment=appointment)

    def test_clinician_type_facility_none(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'clinician_type': 'blahblah',
            'clinician_facility': 'blahblah',
        }
        form_validator = HomeVisitFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_clinician_type_facility_invalid1(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'clinician_type': 'research_team',
            'clinician_facility': 'blah',
        }
        form_validator = HomeVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('clinician_facility', form_validator._errors)

    def test_clinician_type_facility_invalid2(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'clinician_type': 'blah',
            'clinician_facility': None,
        }
        form_validator = HomeVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('clinician_facility', form_validator._errors)

    def test_next_visit_delayed_yes_count_valid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'clinician_type': 'research_team',
            'clinician_facility': None,
        }
        form_validator = HomeVisitFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_visit_outcome_next_appointment_invalid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'visit_outcome': ALIVE,
            'next_appointment': None,
            'next_ap_type': 'blahblah',
        }
        form_validator = HomeVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('next_appointment', form_validator._errors)

    def test_visit_outcome_next_appointment_valid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'visit_outcome': ALIVE,
            'next_appointment': 'blahblah',
             'next_ap_type': 'blahblah',
        }
        form_validator = HomeVisitFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_visit_outcome_next_ap_type_invalid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'visit_outcome': ALIVE,
            'next_ap_type': None,
            'next_appointment': 'blahblah'
        }
        form_validator = HomeVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('next_ap_type', form_validator._errors)

    def test_visit_outcome_next_ap_type_valid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'visit_outcome': ALIVE,
            'next_ap_type': 'blahblah',
            'next_appointment': 'blahblah'
        }
        form_validator = HomeVisitFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_clinician_type_other_invalid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'clinician_type': OTHER,
            'clinician_type_other': None,
        }
        form_validator = HomeVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('clinician_type_other', form_validator._errors)

    def test_clinician_type_other_valid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'clinician_type': OTHER,
            'clinician_type_other': 'blahblah',
        }
        form_validator = HomeVisitFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_clinician_facility_other_invalid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'clinician_facility': OTHER,
            'clinician_facility_other': None,
        }
        form_validator = HomeVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('clinician_facility_other', form_validator._errors)

    def test_clinician_facility_other_valid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'clinician_facility': OTHER,
            'clinician_facility_other': 'blahblah',
        }
        form_validator = HomeVisitFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_visit_outcome_other_invalid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'visit_outcome': OTHER,
            'visit_outcome_other': None,
        }
        form_validator = HomeVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('visit_outcome_other', form_validator._errors)

    def test_visit_outcome_other_valid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'visit_outcome': OTHER,
            'visit_outcome_other': 'blahblah',
        }
        form_validator = HomeVisitFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_next_ap_facility_other_invalid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'next_ap_facility': OTHER,
            'next_ap_facility_other': None,
        }
        form_validator = HomeVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('next_ap_facility_other', form_validator._errors)

    def test_next_ap_facility_other_valid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'next_ap_facility': OTHER,
            'next_ap_facility_other': 'blahblah',
        }
        form_validator = HomeVisitFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
