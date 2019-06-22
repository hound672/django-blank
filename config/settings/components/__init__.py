# -*- coding: utf-8 -*-
"""
    __init__.py
    ~~~~~~~~~~~~~~~
  

"""
import os
from pathlib import PurePath

# determine project's root dir
BASE_DIR = PurePath(__file__).parent.parent.parent.parent


def config(key, default=''):
    """
    Returns environ's value
    """
    return os.environ.get(key, default)


# determine ENV name
ENV = os.environ['ENV']

# debug is true if ENV is not production
DEBUG_MODE = ENV != 'production'
