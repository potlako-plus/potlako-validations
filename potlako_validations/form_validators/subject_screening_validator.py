from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import NO, YES, UNKNOWN
from edc_form_validators import FormValidator


class ScreeningFormValidator(FormValidator):

    clinician_call_enrollment_model = 'potlako_subject.cliniciancallenrollment'

    @property
    def clinician_call_enrollment_cls(self):
        return django_apps.get_model(self.clinician_call_enrollment_model)

    def clean(self):

        try:
            clinician_call_enrollment_obj = self.clinician_call_enrollment_cls.objects.get(
                screening_identifier=self.cleaned_data.get('screening_identifier'))
        except self.clinician_call_enrollment_cls.DoesNotExist:
            raise forms.ValidationError(
                "Participant missing Clinician Call Enrollment form.")
        else:
            enrollment_site = self.cleaned_data.get('enrollment_site')
            if (enrollment_site != clinician_call_enrollment_obj.facility):
                message = {
                    'enrollment_site': 'The enrollment site must match the one in'
                    f'clinician call enrollment form. Got {enrollment_site}, '
                    f'expected {clinician_call_enrollment_obj.facility}'}
                self._errors.update(message)
                raise ValidationError(message)

        self.validate_other_specify(field='enrollment_site', )

        residency_fields = ['residency', 'nationality']

        for residency_field in residency_fields:
            self.applicable_if(
                YES,
                field='enrollment_interest',
                field_applicable=residency_field)

        self.required_if(
            NO,
            field='enrollment_interest',
            field_required='disinterest_reason', )

        self.required_if(
            UNKNOWN,
            field='enrollment_interest',
            field_required='unknown_reason', )

        self.validate_other_specify(field='disinterest_reason', )
