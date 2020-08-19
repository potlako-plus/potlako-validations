from edc_form_validators import FormValidator


class NextOfKinFormValidator(FormValidator):

    def clean(self):
        super().clean()

        self.validate_other_specify(
            'kin_relationship',
            other_specify_field='kin_relation_other')
