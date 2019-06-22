# -*- coding: utf-8 -*-
"""
    settings/dev.py
    ~~~~~~~~~~~~~~~
  
    Настройки для сервера разработки.
"""

# noinspection PyUnresolvedReferences
from config.settings.components.common import *
from config.settings.components import BASE_DIR

# dir for coverage html output
COVERAGE_REPORT_HTML_OUTPUT_DIR = BASE_DIR.joinpath('cover')

# for debug mode allow all hosts
ALLOWED_HOSTS = ['*']

# simple secret key for debug mode
SECRET_KEY = ':xr@79Ca47cL/L]qcuptu$}=.<`J=U4lr1kom3o`HcjO{*j@{k'

# add additions apps for debug mode
INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

DEBUG_TOOLBAR_PATCH_SETTINGS = False

INTERNAL_IPS = [
    '188.243.168.56',  # home IP
    '185.51.60.86'  # satsol office IP
]
