from django.core.exceptions import ValidationError
from edc_constants.constants import YES, NO
from edc_locator.forms import (
    SubjectLocatorFormValidator as BaseSubjectLocatorFormValidator)


class SubjectLocatorFormValidator(BaseSubjectLocatorFormValidator):

    def validate_indirect_contact(self):
        
        self.required_if(
            YES, field='may_contact_indirectly',
            field_required='indirect_contact_name')
        
        self.required_if(
            YES, field='may_contact_indirectly',
            field_required='indirect_contact_relation')
        
        if self.cleaned_data.get('may_contact_indirectly') == YES:
            if (not self.cleaned_data.get('indirect_contact_cell') and
                not self.cleaned_data.get('indirect_contact_phone')):
                message = {'may_contact_indirectly':
                       ('Please provide either cell number or telephone number'
                       ' of next of kin.')}
                self._errors.update(message)
                raise ValidationError(message)
        
        self.not_applicable_if(
            NO, field='may_contact_indirectly',
            field_applicable='has_alt_contact')

    def validate_work_contact(self):
        may_call_work = self.cleaned_data.get('may_call_work')
        workplace = self.cleaned_data.get('subject_work_place')
        work_phone = self.cleaned_data.get('subject_work_phone')
        work_cell = self.cleaned_data.get('subject_work_cell')

        if may_call_work == YES and not workplace and not work_phone and not work_cell:
            message = {'may_call_work':
                       'Please provide any of the work details below.'}
            self._errors.update(message)
            raise ValidationError(message)

        responses = (NO, 'doesnt_work')
        fields = ['subject_work_place', 'subject_work_phone', 'subject_work_cell']
        for field in fields:
            self.not_required_if(
                *responses,
                field='may_call_work',
                field_required=field,
                inverse=False, )

    def clean(self):
        super().clean()
        self.required_if(
            YES, field='may_visit_home',
            field_required='physical_address')

        for field in ['alt_contact_name', 'alt_contact_rel']:
            self.required_if(
                YES, field='has_alt_contact',
                field_required=field)

        has_alt_contact = self.cleaned_data.get('has_alt_contact')
        alt_contact_cell = self.cleaned_data.get('alt_contact_cell')
        alt_contact_tel = self.cleaned_data.get('alt_contact_tel')

        if has_alt_contact == YES:

            if not (alt_contact_cell or alt_contact_tel):
                message = {'alt_contact_cell':
                           'A cell number or telephone number is required'}
                self._errors.update(message)
                raise ValidationError(message)

        for field in ['other_alt_contact_cell', 'alt_contact_tel']:
            self.not_required_if(
                NO, field='has_alt_contact', field_required=field,
                inverse=False)

        if self.cleaned_data.get('may_call', None) == YES:
            if (not self.cleaned_data['subject_cell'] and
                    not self.cleaned_data['subject_phone']):
                message = {'may_call':
                           'Please provide the patient\'s cell number or telephone.'}
                self._errors.update(message)
                raise ValidationError(message)

        if not self.cleaned_data['subject_cell'] and self.cleaned_data['subject_cell_alt']:
            message = {'subject_cell_alt':
                       'Please provide the cell number before it\'s alternative'}
            self._errors.update(message)
            raise ValidationError(message)

        if not self.cleaned_data['subject_phone'] and self.cleaned_data['subject_phone_alt']:
            message = {'subject_phone_alt':
                       'Please provide the telephone before it\'s alternative'}
            self._errors.update(message)
            raise ValidationError(message)

        fields = ['subject_cell', 'subject_phone', 'subject_cell_alt', 'subject_phone_alt']
        for field in fields:
            self.not_required_if(
                NO,
                field='may_call',
                field_required=field,
                inverse=False)

        self.not_required_if(
            NO, field='may_contact_indirectly',
            field_required='has_alt_contact',
            not_required_msg='This person should be the next of kin above.')
