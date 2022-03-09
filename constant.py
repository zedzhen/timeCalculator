import string
from os import environ
from os.path import join

LETTER = 'dhms'
MATH_SYMBOL = '+-*/'
MATH_SYMBOL_FULL = MATH_SYMBOL + '().:' 
DIGIT = string.digits

NAME = 'timeCalculator'

DATA_PATH = join(environ['localAppData'], NAME)

VERSION = '1.1'
VERSION_DATE = '09.03.2022'

HOME_URL = 'github.com/zedzhen/' + NAME
UPDATE_URL = 'https://zedzhen.github.io/' + NAME
