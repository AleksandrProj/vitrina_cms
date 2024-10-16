from .base import *

from backend.utils import show_toolbar


DEBUG = False

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
}
