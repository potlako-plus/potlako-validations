from edc_constants.constants import YES
from edc_form_validators import FormValidator


class FacilityVisitFormValidator(FormValidator):

    def clean(self):

        self.subject_identifier = self.cleaned_data.get(
            'patient_call_followup').subject_visit.appointment.subject_identifier

        self.required_if_not_none(
            field='interval_visit_date',
            field_required='interval_visit_date_estimated',)

        self.required_if(
            YES,
            field='interval_visit_date_estimated',
            field_required='interval_visit_date_estimation',)

        self.validate_other_specify(
            'visit_facility')
        
        super().clean()
