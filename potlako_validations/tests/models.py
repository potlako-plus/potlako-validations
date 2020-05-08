from django.apps import apps as django_apps
from django.db import models
from django.db.models.deletion import PROTECT
from django_crypto_fields.fields import FirstnameField, LastnameField
from edc_base.model_mixins import BaseUuidModel, ListModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO, GENDER
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin


class ListModel(ListModelMixin, BaseUuidModel):
    pass


class SubjectConsent(UpdatesOrCreatesRegistrationModelMixin, BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    screening_identifier = models.CharField(max_length=50)

    gender = models.CharField(max_length=25)

    is_literate = models.CharField(max_length=25,
                                   blank=True,
                                   null=True)

    witness_name = models.CharField(max_length=25,
                                    blank=True,
                                    null=True)

    dob = models.DateField()

    consent_datetime = models.DateTimeField()

    version = models.CharField(
        max_length=10,
        editable=False)


class RegisteredSubject(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    first_name = FirstnameField(null=True)

    last_name = LastnameField(verbose_name="Last name")

    gender = models.CharField(max_length=1, choices=GENDER)


class Appointment(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    appt_datetime = models.DateTimeField(default=get_utcnow)

    visit_code = models.CharField(max_length=25)


class SubjectVisit(BaseUuidModel):

    appointment = models.OneToOneField(Appointment, on_delete=PROTECT)

    subject_identifier = models.CharField(max_length=25)

    visit_code = models.CharField(max_length=25)

    visit_code_sequence = models.IntegerField(default=0)

    report_datetime = models.DateTimeField(
        default=get_utcnow)

    def save(self, *args, **kwargs):
        self.visit_code = self.appointment.visit_code
        self.subject_identifier = self.appointment.subject_identifier
        super().save(*args, **kwargs)


class SubjectScreening(BaseUuidModel):

    subject_identifier = models.CharField(
        max_length=50)

    report_datetime = models.DateTimeField(
        null=True,
        blank=True)

    screening_identifier = models.CharField(
        max_length=36,
        unique=True,
        editable=False)

    has_omang = models.CharField(max_length=3)

    age_in_years = age_in_years = models.IntegerField()


class SubjectLocator(BaseUuidModel):

    subject_identifier = models.CharField(
        max_length=50)

    report_datetime = models.DateTimeField(
        null=True,
        blank=True)

    may_sms = models.CharField(
        max_length=3)

    may_call = models.CharField(
        max_length=3)

    may_visit_home = models.CharField(
        max_length=3)
