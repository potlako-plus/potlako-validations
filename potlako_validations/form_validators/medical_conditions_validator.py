from edc_constants.constants import YES
from edc_form_validators import FormValidator


class MedicalConditionsFormValidator(FormValidator):

    def clean(self):

        self.subject_identifier = self.cleaned_data.get(
            'medical_diagnosis').subject_visit.appointment.subject_identifier

        self.required_if(
            YES,
            field='diagnosis_date_estimate',
            field_required='diagnosis_date_estimation',)

        self.required_if(
            YES,
            field='on_medication',
            field_required='treatment_type',)

        self.validate_other_specify(
            'medical_condition')
        
        self.validate_other_specify(
            'treatment_type')

        super().clean()
