from edc_constants.constants import YES
from edc_form_validators import FormValidator
from .crf_form_validator import CRFFormValidator


class InvestigationsOrderedFormValidator(CRFFormValidator, FormValidator):

    def clean(self):

        self.subject_identifier = self.cleaned_data.get(
            'subject_visit').appointment.subject_identifier

        self.m2m_required_if(
            'pathology',
            field='tests_ordered_type',
            m2m_field='pathology_test')

        self.required_if(
            'imaging',
            field='tests_ordered_type',
            field_required='imaging_test_status')

        self.required_if(
            'imaging',
            field='tests_ordered_type',
            field_required='imaging_test_type')

        self.required_if(
            YES,
            field='ordered_date_estimated',
            field_required='ordered_date_estimation')

        self.required_if(
            'FNA',
            field='pathology_test',
            field_required='fna_location',)

        self.required_if(
            'pathology',
            field='tests_ordered_type',
            field_required='pathology_specimen_date',)

        self.required_if(
            YES,
            field='tests_ordered_type',
            field_required='pathology_tests_ordered')

        self.required_if(
            'ultrasound_other',
            field='imaging_test_type',
            field_required='ultrasound_tests',)

        self.required_if(
            'CT',
            field='imaging_test_type',
            field_required='ct_tests',)

        self.required_if(
            'MRI',
            field='imaging_test_type',
            field_required='mri_tests',)

        other_fields = ['facility_ordered', 'imaging_test_type', ]

        for other_field in other_fields:
            self.validate_other_specify(
                other_field)

        super().clean()
