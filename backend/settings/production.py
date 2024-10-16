import os

from .base import *

from backend.utils import show_toolbar, str_to_bool


DEBUG = str_to_bool(os.environ.get("IS_DEBUG", "False"))

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
}
