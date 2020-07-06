from django.apps import apps as django_apps
from edc_constants.constants import NO, YES, OTHER, NOT_APPLICABLE
from edc_form_validators import FormValidator
from .crf_form_validator import CRFFormValidator
from django.core.exceptions import ValidationError


class PatientCallFuFormValidator(CRFFormValidator, FormValidator):

    patient_call_fu_model = 'potlako_subject.patientcallfollowup'

    @property
    def patient_call_fu_cls(self):
        return django_apps.get_model(self.patient_call_fu_model)

    def clean(self):
        self.validate_first_specialist_visit()

        self.subject_identifier = self.cleaned_data.get(
            'subject_visit').appointment.subject_identifier

        fields = ['visit_delayed_count', 'visit_delayed_reason',
                  'patient_factor', 'health_system_factor',
                  'delayed_visit_description', ]
        for field in fields:
            if field in self.cleaned_data:
                self.not_required_if(
                    NO,
                    field='next_visit_delayed',
                    field_required=field,)

        fields = {'new_complaints': 'new_complaints_description',
                  'appt_change': 'appt_change_reason'}

        for field, required_field in fields.items():
            self.required_if(
                YES,
                field=field,
                field_required=required_field)

        for field in ['facility_visited_count', 'last_visit_date',
                      'last_visit_date_estimated', 'last_visit_facility']:
            self.required_if(
                YES,
                field='interval_visit',
                field_required=field)

        self.required_if(
            YES,
            field='last_visit_date_estimated',
            field_required='last_visit_date_estimation')

        self.required_if(
            NO,
            field='transport_support_received',
            field_required='transport_details')

        fields = {'clinician_communication_issues': 'clinician_issues_details',
                  'communication_issues': 'issues_details',
                  'other_issues': 'other_issues_details'}

        for field, required_field in fields.items():
            self.required_if(
                YES,
                field=field,
                field_required=required_field)

        self.validate_other_specify(
            'next_ap_facility',
            other_specify_field='next_ap_facility_other',)

        fields_other = ['appt_change_reason', 'sms_outcome']
        for field_other in fields_other:
            self.validate_other_specify(field=field_other)

        self.m2m_other_specify(
            OTHER,
            m2m_field='call_achievements',
            field_other='call_achievements_other')

        self.validate_next_appointment_date(
            next_ap_date=self.cleaned_data.get('next_appointment_date'))

        super().clean()

    def validate_first_specialist_visit(self):
        subject_identifier = self.cleaned_data.get(
            'subject_visit').subject_identifier
        qs = self.patient_call_fu_cls.objects.filter(
            subject_visit__subject_identifier=subject_identifier)
        if self.instance.pk is not None:
            qs = qs.exclude(pk=self.instance.pk)

        responses = list()
        for patient_call_fu in qs:
            responses.append(patient_call_fu.first_specialist_visit)

        first_specialist_visit = self.cleaned_data.get(
            'first_specialist_visit')
        if YES in responses and first_specialist_visit != NOT_APPLICABLE:
            message = {
                'first_specialist_visit': 'This field is not applicable'}
            self._errors.update(message)
            raise ValidationError(message)
