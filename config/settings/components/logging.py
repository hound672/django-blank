# -*- coding: utf-8 -*-
"""
    logging
    ~~~~~~~~~~~~~~~
  
    file for logging settings
"""

from config.settings.components import BASE_DIR, config
from pathlib import PurePath

# determine log dir
LOG_DIR = PurePath(config('LOG_DIR', BASE_DIR.joinpath('log')))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'formatters': {
        'main_formatter': {
            'format': '[%(asctime)s]-[%(levelname)s:%(name)s]-'
                      '[%(filename)s:%(lineno)d]: %(message)s',
            'datefmt': "%d-%m-%y %H:%M:%S",
        },
        'console_formatter': {
            'format': '***** [%(levelname)s:%(name)s]-'
                      '[%(filename)s:%(lineno)d]: %(message)s',
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'include_html': True,
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'console_formatter',
        },
        'py_warnings': {
            'level': 'WARNING',
            'class': 'utils.logging.TimedRotatingFileHandlerEx',
            'formatter': 'main_formatter',
            'filename': LOG_DIR.joinpath('py_warnings.log')
        },
        'common_logger': {
            'level': 'INFO',
            'class': 'utils.logging.TimedRotatingFileHandlerEx',
            'formatter': 'main_formatter',
            'filename': LOG_DIR.joinpath('common.log')
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
        },
        'py.warnings': {
            'handlers': ['py_warnings'],
        },
        '': {
            'level': 'INFO',
            'handlers': ['console', 'common_logger'],
        },
    }
}
