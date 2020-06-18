from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import NO, YES

from ..form_validators import TransportFormValidator
from .models import ListModel
from .models import SubjectConsent, SubjectVisit, Appointment


class TestTransportForm(TestCase):

    def setUp(self):
        ListModel.objects.create(name='disability')
        ListModel.objects.create(name='bus')

        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111', consent_datetime=get_utcnow(),
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date())
        appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000')
        self.subject_visit = SubjectVisit.objects.create(
            appointment=appointment)

    def test_criteria_met_yes_trans_type_required(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'is_criteria_met': YES,
            'criteria_met': ListModel.objects.all(),
            'transport_type': None}

        form_validator = TransportFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('transport_type', form_validator._errors)

    def test_criteria_met_no_trans_type_invalid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'is_criteria_met': NO,
            'transport_type': ListModel.objects.filter(name='bus')}
        form_validator = TransportFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
        self.assertIn('transport_type', form_validator._errors)

    def test_criteria_met_yes_trans_type_valid(self):

        cleaned_data = {
            'subject_visit': self.subject_visit,
            'is_criteria_met': YES,
            'criteria_met': ListModel.objects.filter(name='disability'),
            'transport_type': ListModel.objects.filter(name='bus')}
        form_validator = TransportFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_criteria_met_no_trans_type_valid(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'is_criteria_met': NO,
            'transport_type': None}
        form_validator = TransportFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
