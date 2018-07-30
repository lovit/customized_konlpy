name = "ckonlpy"
__title__ = 'customized-konlpy'
__version__ = '0.0.62'
__author__ = 'Lovit'
__license__ = 'GPL v3'
__copyright__ = 'Copyright 2017 Lovit'

from .dictionary import CustomizedDictionary
from .utils import installpath
from .utils import load_dictionary
from .utils import loadtxt
from .utils import load_wordset
from .utils import load_replace_wordpair
from .utils import load_ngram
from . import custom_tag
from . import tag