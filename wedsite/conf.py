from wedsite.settings import (DEFAULT_JSON, DEFAULT_ACCESS)
from django.conf import settings
from appconf import AppConf

class WedsiteAppConf(AppConf):
    """
    Application configuration class. Helps us to have some default settings
    for the wedsite module but allow users to override them.
    """
    JSON = DEFAULT_JSON
    ACCESS = DEFAULT_ACCESS