# -*- coding: utf-8 -*-
"""
    settings/__init__.py
    ~~~~~~~~~~~~~~~
  
"""

from .components import ENV

# import common settings
from config.settings.components.version import *
from config.settings.components.logging import *

# choice and import settings for type build
if ENV == 'production':
    from config.settings.environments.production import *
else:
    from config.settings.environments.develop import *
