from edc_constants.constants import OTHER, NO, YES
from edc_form_validators import FormValidator
from .crf_form_validator import CRFFormValidator


class TransportFormValidator(CRFFormValidator, FormValidator):

    def clean(self):

        self.subject_identifier = self.cleaned_data.get(
            'subject_visit').appointment.subject_identifier

        other_fields = ['visit_facility', 'vehicle_status',
                        'bus_voucher_status', 'transport_type']
        for field in other_fields:
            self.validate_other_specify(field)

        self.m2m_other_specify(
            OTHER,
            m2m_field='criteria_met',
            field_other='criteria_met_other')

        self.not_applicable_if(
            NO,
            field='is_criteria_met',
            field_applicable='transport_type')

        self.m2m_required_if(
            YES,
            field='is_criteria_met',
            m2m_field='criteria_met')
        
        self.validate_other_specify(
            field='cash_transfer_status',
            other_stored_value='not_successful')

        field_responses = {
            'vehicle_status': ('facility_vehicle', 'patient_arranged_vehicle'),
            'bus_voucher_status': ('bus',),
            'cash_transfer_status': ('cash',)}

        for field_applicable, responses in field_responses.items():
            self.applicable_if(
                *responses,
                field='transport_type',
                field_applicable=field_applicable)

        super().clean()
