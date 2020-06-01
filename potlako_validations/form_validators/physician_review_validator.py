from edc_form_validators import FormValidator
from .crf_form_validator import CRFFormValidator


class PhysicianReviewFormValidator(CRFFormValidator, FormValidator):

    def clean(self):

        self.subject_identifier = self.cleaned_data.get(
            'subject_visit').appointment.subject_identifier

        other_fields = ['reviewer_name', 'non_cancer_diagnosis',
                        'cancer_diagnosis', ]

        for other_field in other_fields:
            self.validate_other_specify(
                other_field)

        super().clean()
