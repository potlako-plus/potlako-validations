from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO

from ..form_validators import ClinicianCallEnrollmentFormValidator


class TestClinicianCallEnrollmentForm(TestCase):

    def test_form_valid(self):
        cleaned_data = {
            'screening_identifier': '1111111',
            'contact_date': get_utcnow(),
            'info_from_clinician': YES,
            'call_clinician_type': 'blah',
            'received_training': YES,
            'consented_contact': YES,
            'facility': 'blah',
            'facility_unit': 'blah',
            'national_identity': '910221439',
            'last_name': 'TEST',
            'first_name': 'TEST',
            'dob': get_utcnow() - relativedelta(years=22),
            'age_in_years': 22,
            'gender': 'F',
            'village_town': 'blah',
            'kgotla': 'blah',
            'nearest_facility': 'blah',
            'primary_cell': '72918270',
            'kin_lastname': 'TEST',
            'kin_firstname': 'ONE',
            'kin_cell': '71329182',
            'other_kin_avail': NO
        }
        form_validator = ClinicianCallEnrollmentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
