# from django.core.exceptions import ValidationError
# from django.test import TestCase
# from edc_constants.constants import NO, YES
#
# from ..form_validators import PatientCallInitialFormValidator
#
#
# class TestPatientCallInitialForm(TestCase):
#
#     def test_next_visit_delayed_no_count_none(self):
#         cleaned_data = {
#             'next_visit_delayed': NO,
#             'visit_delayed_count': None,
#         }
#         form_validator = PatientCallInitialFormValidator(
#             cleaned_data=cleaned_data)
#         try:
#             form_validator.validate()
#         except ValidationError as e:
#             self.fail(f'ValidationError unexpectedly raised. Got{e}')
#
#     def test_next_visit_delayed_no_count_invalid(self):
#         cleaned_data = {
#             'next_visit_delayed': NO,
#             'visit_delayed_count': 1,
#         }
#         form_validator = PatientCallInitialFormValidator(
#             cleaned_data=cleaned_data)
#         self.assertRaises(ValidationError, form_validator.clean)
#         self.assertIn('visit_delayed_count', form_validator._errors)
#
#     def test_next_visit_delayed_yes_count_valid(self):
#         cleaned_data = {
#             'next_visit_delayed': YES,
#             'visit_delayed_count': 1,
#         }
#         form_validator = PatientCallInitialFormValidator(
#             cleaned_data=cleaned_data)
#         try:
#             form_validator.validate()
#         except ValidationError as e:
#             self.fail(f'ValidationError unexpectedly raised. Got{e}')
#
#     def test_next_visit_delayed_yes_count_none(self):
#         cleaned_data = {
#             'next_visit_delayed': YES,
#             'visit_delayed_count': None,
#         }
#         form_validator = PatientCallInitialFormValidator(
#             cleaned_data=cleaned_data)
#         self.assertRaises(ValidationError, form_validator.clean)
#         self.assertIn('visit_delayed_count', form_validator._errors)
#
#     def test_next_visit_delayed_no_reason_none(self):
#         cleaned_data = {
#             'next_visit_delayed': NO,
#             'visit_delayed_reason': None,
#         }
#         form_validator = PatientCallInitialFormValidator(
#             cleaned_data=cleaned_data)
#         try:
#             form_validator.validate()
#         except ValidationError as e:
#             self.fail(f'ValidationError unexpectedly raised. Got{e}')
#
#     def test_next_visit_delayed_no_reason_invalid(self):
#         cleaned_data = {
#             'next_visit_delayed': NO,
#             'visit_delayed_reason': 'Reason',
#         }
#         form_validator = PatientCallInitialFormValidator(
#             cleaned_data=cleaned_data)
#         self.assertRaises(ValidationError, form_validator.clean)
#         self.assertIn('visit_delayed_reason', form_validator._errors)
#
#     def test_next_visit_delayed_yes_reason_none(self):
#         cleaned_data = {
#             'next_visit_delayed': YES,
#             'visit_delayed_reason': None,
#         }
#         form_validator = PatientCallInitialFormValidator(
#             cleaned_data=cleaned_data)
#         self.assertRaises(ValidationError, form_validator.clean)
#         self.assertIn('visit_delayed_reason', form_validator._errors)
#
#     def test_next_visit_delayed_yes_reason_valid(self):
#         cleaned_data = {
#             'next_visit_delayed': YES,
#             'visit_delayed_reason': 'Reason',
#         }
#         form_validator = PatientCallInitialFormValidator(
#             cleaned_data=cleaned_data)
#         try:
#             form_validator.validate()
#         except ValidationError as e:
#             self.fail(f'ValidationError unexpectedly raised. Got{e}')
