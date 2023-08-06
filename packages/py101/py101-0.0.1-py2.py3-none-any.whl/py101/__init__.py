from story.story import BaseStory
from story.translation import gettext as _

from . import (introduction,)


__author__ = """Sophilabs"""
__email__ = 'hi@sophilabs.co'
__version__ = '0.0.1'


class Story(BaseStory):
    "Python Essentials Adventure"
    name = 'py101'
    title = _('Learn Python essentials using the command line')
    adventures = [
        introduction
    ]
