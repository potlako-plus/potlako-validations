from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_base.utils import age, get_utcnow
from edc_constants.constants import MALE, FEMALE
from edc_form_validators import FormValidator


class SubjectConsentFormValidator(FormValidator):

    clinician_call_enrollment_model = 'potlako_subject.cliniciancallenrollment'

    subject_screening_model = 'potlako_subject.subjectscreening'

    @property
    def subject_screening_cls(self):
        return django_apps.get_model(self.subject_screening_model)

    @property
    def clinician_call_enrollment_cls(self):
        return django_apps.get_model(self.clinician_call_enrollment_model)

    def clean(self):
        self.screening_identifier = self.cleaned_data.get('screening_identifier')

        try:
            clinician_enrollment = self.clinician_call_enrollment_cls.objects.get(
                screening_identifier=self.screening_identifier)
        except self.clinician_call_enrollment_cls.DoesNotExist:
            raise ValidationError('Please complete the Clinician Call '
                                  'Enrollment form first.')
        else:
            self.validate_personal_fields(clinician_enrollment.last_name,
                                          field='last_name')
            self.validate_personal_fields(clinician_enrollment.first_name,
                                          field='first_name')
            self.validate_personal_fields(clinician_enrollment.gender,
                                          field='gender')
            if self.cleaned_data.get('identity_type') == 'country_id':
                self.validate_personal_fields(
                    clinician_enrollment.national_identity,
                    field='identity')

        self.validate_dob(self.screening_identifier)
        self.validate_identity_gender()

    def validate_identity_gender(self):

        identity_key = self.cleaned_data.get('identity')[4]
        gender = self.cleaned_data.get('gender')

        if gender == MALE and identity_key != '1':
            message = {'national_identity': 'The national identity number '
                       f'does not match the pattern expected. Expected the '
                       f'fourth digit as \'1\' for male, got \'{identity_key}\''}
            self._errors.update(message)
            raise ValidationError(message)
        elif gender == FEMALE and identity_key != '2':
            message = {'identity': 'The national identity number '
                       f'does not match the pattern expected. Expected the '
                       f'fourth digit as \'2\' for female, got \'{identity_key}\''}
            self._errors.update(message)
            raise ValidationError(message)

    def validate_dob(self, screening_identifier):
        try:
            subject_screening = self.subject_screening_cls.objects.get(
                screening_identifier=screening_identifier)
        except self.subject_screening_cls.DoesNotExist:
            raise ValidationError('Please complete the Potlako+ Eligibility '
                                  'form first.')
        else:
            dob = self.cleaned_data.get('dob')
            age_in_years = age(dob, get_utcnow()).years

            if (subject_screening.age_in_years
                    and subject_screening.age_in_years != age_in_years):
                message = {'dob':
                           'The age derived from Date of birth does not '
                           'match the age provided in the Potlako+ Eligibility'
                           f' form. Expected \'{subject_screening.age_in_years}\' '
                           f'got \'{age_in_years}\''}
                self._errors.update(message)
                raise ValidationError(message)

    def validate_personal_fields(self, clinician_call_value=None, field=None):

        field_value = self.cleaned_data.get(field)
        clinician_call_value

        if clinician_call_value != field_value:
            message = {field:
                       f'The {field} provided does not match the {field} '
                       f'provided in the Clinician Call Enrollment '
                       f' form. Expected \'{clinician_call_value}\' '
                       f'got \'{field_value}\''}
            self._errors.update(message)
            raise ValidationError(message)
