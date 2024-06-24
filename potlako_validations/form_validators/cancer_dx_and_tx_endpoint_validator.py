from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import YES
from edc_form_validators import FormValidator


class CancerDxAndTxEndpointFormValidator(FormValidator):
    care_seeking_endpoint_model = 'potlako_subject.symptomsandcareseekingendpoint'

    @property
    def care_seeking_endpoint_cls(self):
        return django_apps.get_model(self.care_seeking_endpoint_model)

    def clean(self):
        self.validate_care_seeking_endpoint_completed()

        req_fields = ['diagnosis_date', 'diagnosis_date_estimated']
        for req_field in req_fields:
            self.required_if(
                'complete',
                field='cancer_evaluation',
                field_required=req_field)

        self.required_if(
            YES,
            field='diagnosis_date_estimated',
            field_required='diagnosis_date_estimation')

        cancer_responses = ['confirmed_cancer', 'probable_cancer']
        self.required_if(
            *cancer_responses,
            field='clinical_impression',
            field_required='icd_10_code')

        cancer_responses = ['confirmed_cancer', 'probable_cancer']
        self.required_if(
            *cancer_responses,
            field='clinical_impression',
            field_required='final_cancer_diagnosis')

        self.validate_other_specify(field='final_cancer_diagnosis')

        self.not_required_if(
            *cancer_responses,
            field='clinical_impression',
            field_required='non_cancer_diagnosis')

        self.validate_other_specify(field='non_cancer_diagnosis')

        required_fields = ['cancer_diagnosis_stage', 'cancer_therapy']
        for required_field in required_fields:
            self.required_if(
                *cancer_responses,
                field='clinical_impression',
                field_required=required_field)

        cancer_stages = ['tumor_stage', 'nodal_stage',
                         'distant_metastasis_stage', ]
        clinical_impression = self.cleaned_data.get('clinical_impression')

        for cancer_stage in cancer_stages:
            if (clinical_impression in cancer_responses
                    and self.cleaned_data.get(cancer_stage) is None):
                msg = {cancer_stage: 'This field is required.'}
                self._errors.update(msg)
                raise ValidationError(msg)
            elif (clinical_impression not in cancer_responses
                  and self.cleaned_data.get(cancer_stage) is not None):
                msg = {cancer_stage: 'This field is not required.'}
                self._errors.update(msg)
                raise ValidationError(msg)

        fields_required = ['treatment_intent', 'therapeutic_surgery',
                           'chemotherapy', 'radiation']
        for field_required in fields_required:
            self.required_if(
                YES,
                field='cancer_therapy',
                field_required=field_required)

        req_fields = ['surgery_date', 'surgery_date_estimated']
        for req_field in req_fields:
            self.required_if(
                YES,
                field='therapeutic_surgery',
                field_required=req_field)

        self.required_if(
            YES,
            field='surgery_date_estimated',
            field_required='surgery_date_estimation')

        req_fields = ['chemotherapy_date', 'chemotherapy_date_estimated']
        for req_field in req_fields:
            self.required_if(
                YES,
                field='chemotherapy',
                field_required=req_field)

        self.required_if(
            YES,
            field='chemotherapy_date_estimated',
            field_required='chemotherapy_date_estimation')

        req_fields = ['radiation_date', 'radiation_date_estimated']
        for req_field in req_fields:
            self.required_if(
                YES,
                field='radiation',
                field_required=req_field)

        self.required_if(
            YES,
            field='radiation_date_estimated',
            field_required='radiation_date_estimation')

    def validate_care_seeking_endpoint_completed(self):
        """Validates that the care seeking endpoint is completed before
        the cancer diagnosis and treatment endpoint is completed.
        """
        try:
            self.care_seeking_endpoint_cls.objects.get(
                subject_identifier=self.cleaned_data.get('subject_identifier'))
        except self.care_seeking_endpoint_cls.DoesNotExist:
            msg = {'final_deposition': 'Care seeking endpoint must be completed first.'}
            self._errors.update(msg)
            raise ValidationError(msg)
