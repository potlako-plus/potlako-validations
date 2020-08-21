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

        if not kin_cell and not kin_telephone:
            message = 'A cell number or telephone number is required'
            raise ValidationError(message)
