from edc_constants.constants import YES, OTHER
from edc_form_validators import FormValidator
from .crf_form_validator import CRFFormValidator


class TransportFormValidator(CRFFormValidator, FormValidator):

    def clean(self):

        self.m2m_required_if(
            YES,
            field='is_criteria_met',
            m2m_field='transport_type',)

        self.m2m_required_if(
            response=YES,
            field='is_criteria_met',
            m2m_field='criteria_met')

        other_fields = ['visit_facility', 'vehicle_status',
                        'bus_voucher_status', 'transport_type']
        for field in other_fields:
            self.validate_other_specify(field)

        m2m_fields = ['criteria_met', 'housemate']

        for m2m_field in m2m_fields:
            self.m2m_other_specify(OTHER,
                                   m2m_field=m2m_field,
                                   field_other=m2m_field + '_other')

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
