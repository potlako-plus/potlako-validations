from edc_form_validators import FormValidator
from django.core.exceptions import ValidationError


class NextOfKinFormValidator(FormValidator):

    def clean(self):
        super().clean()

        self.validate_other_specify(
            'kin_relationship',
            other_specify_field='kin_relation_other')

        kin_cell = self.cleaned_data.get('kin_cell')
        kin_telephone = self.cleaned_data.get('kin_telephone')

        if kin_cell == '' and kin_telephone == '':
            message = {'kin_cell':
                       'A cell number or',
                       'kin_telephone':
                       'telephone number is required'}
            self._errors.update(message)
            raise ValidationError(message)
