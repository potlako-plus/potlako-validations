from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import NO, OTHER, YES
from edc_form_validators import FormValidator


class PatientCallInitialFormValidator(FormValidator):

    def clean(self):
        self.required_if(
            YES,
            field='work_status',
            field_required='work_type',)

        self.required_if(
            YES,
            field='potlako_sms_received',
            field_required='sms_platform',)

        self.required_if(
            NO,
            field='work_status',
            field_required='unemployed_reason',)

        self.required_if(
            YES,
            field='patient_symptoms_date_estimated',
            field_required='patient_symptoms_date_estimation',)

        self.not_required_if(
            0,
            field='symptoms_duration_report',
            field_required='symptoms_duration',)

        self.not_required_if(
            NO,
            field='other_facility',
            field_required='facility_number',)

        other_fields = ['primary_clinic', 'work_type', 'source_of_info',
                        'residential_district', 'unemployed_reason',
                        'enrollment_visit_method', 'next_ap_facility',
                        'next_ap_facility_unit']

        for other_field in other_fields:
            self.validate_other_specify(
                other_field)

        self.required_if(
            YES,
            field='heard_of_potlako',
            field_required='source_of_info')

        self.m2m_required_if(
            YES,
            field='potlako_sms_received',
            m2m_field='sms_platform')

        self.m2m_other_specify(
            OTHER,
            m2m_field='sms_platform',
            field_other='sms_platform_other')

        self.m2m_other_specify(
            OTHER,
            m2m_field='patient_residence',
            field_other='patient_residence_other')

        self.m2m_other_specify(
            OTHER,
            m2m_field='call_achievements',
            field_other='call_achievements_other')

        self.required_if_not_none(
            field='hiv_test_date',
            field_required='hiv_test_date_estimated',)

        self.required_if(
            YES,
            field='hiv_test_date_estimated',
            field_required='hiv_test_date_estimation',)

#     def update_locator_fields(self):
#         subject_locator_cls = django_apps.get_model(
#             'potlako_subject.subjectlocator')
#
#         try:
#             subject_locator_cls.objects.get(
#                 subject_identifier=self.cleaned_data.get(
#                     'subject_visi').appointment.subject_identifier)
#         except subject_locator_cls.DoesNotExist:
#             raise ValidationError(
#                 'Please complete Subject Locator form '
#                 f'before  proceeding.')
#         else:
#             'residential_district'
#             'patient_kgotla', 'patient_number', 'patient_contact'
