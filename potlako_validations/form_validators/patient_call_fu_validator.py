from edc_constants.constants import NO
from edc_form_validators import FormValidator


class PatientCallFuFormValidator(FormValidator):

    def clean(self):

        fields = ['visit_delayed_count', 'visit_delayed_reason',
                  'patient_factor', 'health_system_factor',
                  'delayed_visit_description', ]
        for field in fields:
            if field in self.cleaned_data:
                self.not_required_if(
                    NO,
                    field='next_visit_delayed',
                    field_required=field, )

        self.validate_other_specify(
            field='patient_factor',
            other_specify_field='patient_factor_other', )

        self.validate_other_specify(
            field='health_system_factor',
            other_specify_field='health_system_factor_other', )

        self.validate_other_specify(
            field='next_ap_facility',
            other_specify_field='next_ap_facility_other', )
