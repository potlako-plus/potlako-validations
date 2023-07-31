from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO

from ..form_validators import CancerDxAndTxFormValidator
from .models import SubjectConsent, SubjectVisit, Appointment


class TestCancerDiagnosisAndTreatmentForm(TestCase):

    def setUp(self):
        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='12345', consent_datetime=get_utcnow(),
            gender='F', dob=(get_utcnow() - relativedelta(years=32)).date())
        appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000')
        self.subject_visit = SubjectVisit.objects.create(
            appointment=appointment)

    def test_complete_eval_diagnosis_date_required(self):
        """
        Assert raises validation error if cancer evaluation is
        complete, but diagnosis date is not specified.
        """
        cleaned_data = {
                'subject_visit': self.subject_visit,
                'cancer_evaluation': 'complete',
                'diagnosis_date': None}

        form_validator = CancerDxAndTxFormValidator(
                cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('diagnosis_date', form_validator._errors)

    def test_complete_eval_diagnosis_date_valid(self):
        """
        Checks that no validation error raised if cancer evaluation is
        complete, and diagnosis date is specified.
        """
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'cancer_evaluation': 'complete',
            'diagnosis_date': get_utcnow() - relativedelta(days=10),
            'diagnosis_date_estimated': NO}

        form_validator = CancerDxAndTxFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_incomplete_eval_diagnosis_date_not_req(self):
        """
        Assert raises validation error if cancer evaluation is not
        completed, but diagnosis date provided
        """
        cleaned_data = {
                'subject_visit': self.subject_visit,
                'cancer_evaluation': 'unable_to_complete',
                'diagnosis_date': get_utcnow() - relativedelta(days=10)}

        form_validator = CancerDxAndTxFormValidator(
                cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('diagnosis_date', form_validator._errors)

    def test_incomplete_eval_diagnosis_date_none(self):
        """
        Checks that no validation error raised if cancer evaluation is not
        completed, and diagnosis date is none (not specified).
        """
        cleaned_data = {
                'subject_visit': self.subject_visit,
                'cancer_evaluation': 'unable_to_complete',
                'diagnosis_date': None}

        form_validator = CancerDxAndTxFormValidator(
                cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_diagnosis_date_estimated_yes_date_estimation_req(self):
        """
        Assert raises validation error if diagnosis date specified
        is an estimate of the date, but diagnosis date estimation is none
        """
        cleaned_data = {
                'subject_visit': self.subject_visit,
                'cancer_evaluation': 'complete',
                'diagnosis_date': get_utcnow() - relativedelta(days=10),
                'diagnosis_date_estimated': YES,
                'diagnosis_date_estimation': None}

        form_validator = CancerDxAndTxFormValidator(
                cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('diagnosis_date_estimation', form_validator._errors)

    def test_diagnosis_date_estimated_yes_date_estimation_valid(self):
        """
        Checks that no validation error raised if diagnosis date specified
        is an estimate, and diagnosis date estimation is specified.
        """
        cleaned_data = {
                'subject_visit': self.subject_visit,
                'cancer_evaluation': 'complete',
                'diagnosis_date': get_utcnow() - relativedelta(days=10),
                'diagnosis_date_estimated': YES,
                'diagnosis_date_estimation': 'day'}

        form_validator = CancerDxAndTxFormValidator(
                cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_cancer_treatment_yes_treatment_desc_req(self):
        """
        Assert raises validation error if cancer treatment is YES,
        but there is no treatment description.
        """
        cleaned_data = {
                'subject_visit': self.subject_visit,
                'cancer_evaluation': 'complete',
                'diagnosis_date': get_utcnow() - relativedelta(days=10),
                'diagnosis_date_estimated': YES,
                'diagnosis_date_estimation': 'day',
                'cancer_treatment': YES,
                'treatment_description': None}

        form_validator = CancerDxAndTxFormValidator(
                cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('treatment_description', form_validator._errors)

    def test_cancer_treatment_yes_treatment_desc_valid(self):
        """
        Checks that no validation error raised if cancer treatment is YES,
        and treatment description is specified.
        """
        cleaned_data = {
                'subject_visit': self.subject_visit,
                'cancer_evaluation': 'complete',
                'diagnosis_date': get_utcnow() - relativedelta(days=10),
                'diagnosis_date_estimated': YES,
                'diagnosis_date_estimation': 'day',
                'cancer_treatment': YES,
                'treatment_description': 'Some very important description'}

        form_validator = CancerDxAndTxFormValidator(
                cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_cancer_treatment_no_treatment_desc_none(self):
        """
        Checks that no validation error raised if cancer treatment is NO,
        and there is no treatment description.
        """
        cleaned_data = {
                'subject_visit': self.subject_visit,
                'cancer_evaluation': 'complete',
                'diagnosis_date': get_utcnow() - relativedelta(days=10),
                'diagnosis_date_estimated': YES,
                'diagnosis_date_estimation': 'day',
                'cancer_treatment': NO,
                'treatment_description': None}
        form_validator = CancerDxAndTxFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
