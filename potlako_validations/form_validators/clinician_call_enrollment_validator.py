from django.core.exceptions import ValidationError
from edc_constants.constants import YES, NO, OTHER
from edc_form_validators import FormValidator


class ClinicianCallEnrollmentFormValidator(FormValidator):

    def clean(self):
        super().clean()

        date_registered = self.cleaned_data.get('reg_date')
        report_datetime = self.cleaned_data.get('report_datetime')

        if date_registered and date_registered > report_datetime.date():
            raise ValidationError('Date patient was registered at facility'
                                  ' should be earlier than report datetime.')

        self.required_if(
            NO,
            field='info_from_clinician',
            field_required='info_source_specify'
        )

        self.required_if(
            YES,
            field='info_from_clinician',
            field_required='call_clinician_type'
        )

        self.validate_other_specify(
            'call_clinician_type',
            other_specify_field='call_clinician_other',
        )

        self.validate_other_specify('facility',)

        self.validate_other_specify(
            'facility_unit',
            other_specify_field='unit_other'
        )

        self.validate_other_specify('nearest_facility',)

        self.validate_other_specify(
            field='kin_relationship',
            other_specify_field='kin_relation_other'
        )

        self.validate_other_specify(
            field='clinician_type',
            other_specify_field='clinician_other'
        )

        self.m2m_other_specify(
            OTHER,
            m2m_field='symptoms',
            field_other='symptoms_other')

        self.required_if(
            YES,
            field='early_symptoms_date_estimated',
            field_required='early_symptoms_date_estimation'
        )

        self.required_if(
            'unsure',
            field='suspected_cancer',
            field_required='suspected_cancer_unsure'
        )

        self.validate_other_specify('suspected_cancer',)

        self.applicable_if(
            'refer',
            field='patient_disposition',
            field_applicable='referral_unit')

        referral_fields = ['referral_reason', 'referral_date',
                           'referral_facility', 'referral_discussed',
                           'clinician_designation', 'referral_fu_date', ]

        for field in referral_fields:
            self.required_if(
                'refer',
                field='patient_disposition',
                field_required=field
            )

        self.validate_other_specify('referral_facility',)

        self.applicable_if(
            YES,
            field='investigated',
            field_applicable='investigation_notes'
        )

        if self.cleaned_data.get('paper_register') == NO:
            message = {'paper_register': 'Please complete patient\'s paper '
                       'register first.'}
            self._errors.update(message)
            raise ValidationError(message)
