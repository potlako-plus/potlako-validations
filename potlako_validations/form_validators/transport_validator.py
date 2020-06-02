from edc_constants.constants import YES
from edc_form_validators import FormValidator
from .crf_form_validator import CRFFormValidator


class TransportFormValidator(CRFFormValidator, FormValidator):

    def clean(self):

        self.subject_identifier = self.cleaned_data.get(
            'subject_visit').appointment.subject_identifier

        self.required_if(
            YES,
            field='is_criteria_met',
            field_required='transport_type',)

        self.m2m_required_if(
            response=YES,
            field='is_criteria_met',
            m2m_field='criteria_met')

        other_fields = ['housemate', 'criteria_met', 'visit_facility',
                        'transport_type', 'vehicle_status', 'bus_voucher_status',
                        'cash_transfer_status']
        for field in other_fields:
            self.validate_other_specify(field)

        super().clean()
