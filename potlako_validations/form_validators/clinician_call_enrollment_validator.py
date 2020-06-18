from django.core.exceptions import ValidationError
from edc_constants.constants import NOT_APPLICABLE
from edc_constants.constants import YES, NO, OTHER, MALE, FEMALE
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
            'call_with_clinician',
            field='cancer_suspect',
            field_required='call_clinician_type')

        self.validate_other_specify(
            field='cancer_suspect',
            other_specify_field='cancer_suspect_other',)

        self.validate_other_specify(
            'call_clinician_type',
            other_specify_field='call_clinician_other',
        )

        consented_contact = self.cleaned_data.get('consented_contact')

        if consented_contact == NO:
            message = {'consented_contact':
                       'The Participant does not consent to being contacted by'
                       ' the Potlako+ team. Can not continue with enrollment.'}
            self._errors.update(message)
            raise ValidationError(message)

        gender = self.cleaned_data.get('gender')
        cancer_type = self.cleaned_data.get('suspected_cancer')

        if (gender == MALE and cancer_type in ['vulva', 'cervical', 'vaginal']):
            message = {'suspected_cancer':
                       'The participant is male, suspected cancer cannot be'
                       f' {cancer_type}. Please correct this.'}
            self._errors.update(message)
            raise ValidationError(message)

        if (gender == FEMALE and cancer_type in ['penile', 'prostate']):
            message = {'suspected_cancer':
                       'The participant is female, suspected cancer cannot be '
                       f'{cancer_type}. Please correct this.'}
            self._errors.update(message)
            raise ValidationError(message)

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

        self.clean_names_start_with_caps()

        identity_key = self.cleaned_data.get('national_identity')[4]
        gender = self.cleaned_data.get('gender')

        if gender == MALE and identity_key != '1':
            message = {'national_identity': 'The national identity number '
                       f'does not match the pattern expected. Expected the '
                       f'fourth digit as \'1\' for male, got {identity_key}'}
            self._errors.update(message)
            raise ValidationError(message)
        elif gender == FEMALE and identity_key != '2':
            message = {'national_identity': 'The national identity number '
                       f'does not match the pattern expected. Expected the '
                       f'fourth digit as \'2\' for female, got {identity_key}'}
            self._errors.update(message)
            raise ValidationError(message)

        self.applicable_if(
            'refer',
            field='patient_disposition',
            field_applicable='referral_unit')

        referral_fields = ['referral_reason', 'referral_facility', ]

        for field in referral_fields:
            self.required_if(
                'refer',
                field='patient_disposition',
                field_required=field
            )

        self.applicable_if(
            'refer',
            field='patient_disposition',
            field_applicable='referral_discussed')

        self.validate_other_specify('referral_facility',)

        responses = ('refer', 'return',)
        self.required_if(
            *responses,
            field='patient_disposition',
            field_required='referral_date')

        self.m2m_single_selection_if(
            NOT_APPLICABLE,
            m2m_field='investigation_notes')

        self.m2m_applicable_if(
            YES,
            field='investigated',
            m2m_field_applicable='investigation_notes'
        )

        self.m2m_other_specify(
            OTHER,
            m2m_field='investigation_notes',
            field_other='investigation_notes_other')

        if self.cleaned_data.get('paper_register') == NO:
            message = {'paper_register': 'Please complete patient\'s paper '
                       'register first.'}
            self._errors.update(message)
            raise ValidationError(message)

        self.required_if(
            YES,
            field='referral_discussed',
            field_required='clinician_designation')

        self.validate_other_specify(field='referral_unit')

    def clean_names_start_with_caps(self):

        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')

        if last_name and not last_name[0].isupper():
            message = {'last_name': 'Must start with capital letter.'}
            self._errors.update(message)
            raise ValidationError(message)
        if first_name and not first_name[0].isupper():
            message = {'first_name': 'Must start with capital letter.'}
            self._errors.update(message)
            raise ValidationError(message)

    def m2m_applicable_if(self, *responses, field=None, m2m_field_applicable=None):

        qs = self.cleaned_data.get(m2m_field_applicable)
        if qs and qs.count() >= 1:
            selected = {obj.short_name: obj.name for obj in qs}
            if (self.cleaned_data.get(field) in responses and
                    NOT_APPLICABLE in selected):
                message = {
                    m2m_field_applicable:
                    'This field is applicable.'}
                self._errors.update(message)
                raise ValidationError(message)
            elif (self.cleaned_data.get(field) not in responses and
                    NOT_APPLICABLE not in selected):
                message = {
                    m2m_field_applicable:
                    'This field is not applicable.'}
                self._errors.update(message)
                raise ValidationError(message)

