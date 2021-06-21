from edc_form_validators import FormValidator
from .crf_form_validator import CRFFormValidator


class InvestigationsResultedFormValidator(CRFFormValidator, FormValidator):

    def clean(self):

        self.subject_identifier = self.cleaned_data.get(
            'subject_visit').appointment.subject_identifier

        self.m2m_other_specify(
            'pathology',
            m2m_field='tests_resulted_type',
            field_other='pathology_tests')

        self.m2m_other_specify(
            'imaging',
            m2m_field='tests_resulted_type',
            field_other='imaging_tests')

        pathology_tests_fields = [
            'pathology_specimen_date', 'pathology_nhl_date',
            'pathology_result_date', 'pathology_received_date',
            'pathology_communicated_date']

        for field in pathology_tests_fields:
            self.m2m_other_specify(
                'pathology',
                m2m_field='tests_resulted_type',
                field_other=field)

        self.m2m_other_specify(
                'imaging',
                m2m_field='tests_resulted_type',
                field_other='imaging_tests_date')

        self.validate_other_specify(
            'diagnosis_results')

        self.required_if(
            'malignant',
            field='diagnosis_results',
            field_required='cancer_type')

        self.required_if(
            'non_malignant',
            field='diagnosis_results',
            field_required='diagnoses_made')

        super().clean()
