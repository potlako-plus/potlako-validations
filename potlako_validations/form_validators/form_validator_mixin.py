from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError


class FormValidatorMixin:

    clinician_call_enrollment_model = 'potlako_subject.cliniciancallenrollment'
    subject_consent_model = 'potlako_subject.subjectconsent'
    subject_screening_model = 'potlako_subject.subjectscreening'

    @property
    def clinician_call_enrollment_cls(self):
        return django_apps.get_model(self.clinician_call_enrollment_model)

    @property
    def subject_consent_cls(self):
        return django_apps.get_model(self.subject_consent_model)

    @property
    def subject_screening_cls(self):
        return django_apps.get_model(self.subject_screening_model)

    def validate_against_consent(self, id=None):
        """Returns an instance of the current subject consent version form or
        raises an exception if not found."""
        if not id:
            try:
                return self.subject_consent_cls.objects.get(
                    subject_identifier=self.subject_identifier).order_by(
                        '-consent_datetime').first()
            except self.subject_consent_cls.DoesNotExist:
                raise ValidationError(
                    'Please complete Subject Consent form '
                    f'before  proceeding.')
