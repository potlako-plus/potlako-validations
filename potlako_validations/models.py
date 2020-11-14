from django.conf import settings

if settings.APP_NAME == 'potlako_validations':
    from .tests import models
