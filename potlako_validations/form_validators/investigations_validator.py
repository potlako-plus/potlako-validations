from edc_constants.constants import YES
from edc_form_validators import FormValidator
from .crf_form_validator import CRFFormValidator


class InvestigationsFormValidator(CRFFormValidator, FormValidator):

    def clean(self):

        self.subject_identifier = self.cleaned_data.get(
            'subject_visit').appointment.subject_identifier

        lab_fields = ['facility_ordered',
                      'ordered_date',
                      'ordered_date_estimated', ]

        for field in lab_fields:
            self.required_if(
                YES,
                field='lab_tests_ordered',
                field_required=field)

        self.required_if(
            YES,
            field='ordered_date_estimated',
            field_required='ordered_date_estimation')

        pathology_fields = ['pathology_test',
                            'pathology_specimen_date',
                            'pathology_nhl_date',
                            'pathology_result_date',
                            'pathology_received_date',
                            'pathology_communicated_date']

        self.required_if(
            'FNA',
            field='pathology_test',
            field_required='fna_location',)

        self.required_if(
            'biopsy_other',
            field='pathology_test',
            field_required='biopsy_other',)

        for field in pathology_fields:
            self.required_if(
                YES,
                field='pathology_tests_ordered',
                field_required=field)

        imaging_fields = ['imaging_test_status',
                          'imaging_test_type',
                          'imaging_tests_date', ]

        for field in imaging_fields:
            self.required_if(
                YES,
                field='imaging_tests',
                field_required=field)

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
