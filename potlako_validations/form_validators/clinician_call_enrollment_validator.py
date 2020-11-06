from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import NOT_APPLICABLE
from edc_constants.constants import YES, NO, OTHER, MALE, FEMALE
from edc_form_validators import FormValidator


class ClinicianCallEnrollmentFormValidator(FormValidator):

    @property
    def facility_app_config(self):
        return django_apps.get_app_config('edc_facility')

    def clean(self):
        super().clean()

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

        if self.cleaned_data.get('paper_register') == NO:
            message = {'paper_register': 'Please complete patient\'s paper '
                       'register first.'}
            self._errors.update(message)
            raise ValidationError(message)

        self.validate_other_specify(field='referral_unit')

        patient_contact = self.cleaned_data['patient_contact']

        if patient_contact == YES:
            if (not self.cleaned_data['primary_cell']
                    and not self.cleaned_data['telephone_number']):
                message = {'patient_contact':
                           'Please provide the patient\'s primary cell number '
                           'or telephone number.'}
                self._errors.update(message)
                raise ValidationError(message)

        fields = ['primary_cell', 'secondary_cell', 'telephone_number']
        for field in fields:
            self.not_required_if(
                NO,
                field='patient_contact',
                field_required=field,
                inverse=False, )

        secondary_cell = self.cleaned_data['secondary_cell']

        if secondary_cell and not self.cleaned_data['primary_cell']:
            message = {'secondary_cell':
                       'Please provide the patient\'s primary cell before their'
                       ' secondary'}
            self._errors.update(message)
            raise ValidationError(message)
        
        if self.cleaned_data['referral_date']:
            if self.cleaned_data['reg_date'] >= self.cleaned_data['referral_date']:
                message = {'referral_date':
                           'Next appointment date cannot be before registration date.'}
                self._errors.update(message)
                raise ValidationError(message)

        self.required_if(
            YES,
            field='investigated',
            field_required='tests_ordered', )

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

    def m2m_applicable_if(
            self, *responses, field=None, m2m_field_applicable=None):

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
