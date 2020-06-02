from edc_constants.constants import NO, YES
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

        self.validate_other_specify(
            'next_ap_facility',
            other_specify_field='next_ap_facility_other',)

        self.validate_next_appointment_date(
            next_ap_date=self.cleaned_data.get('next_ap_date'))

        super().clean()
