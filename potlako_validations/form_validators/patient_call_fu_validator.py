from edc_constants.constants import NO, YES, OTHER
from edc_form_validators import FormValidator
from .crf_form_validator import CRFFormValidator


class PatientCallFuFormValidator(CRFFormValidator, FormValidator):

    def clean(self):

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
