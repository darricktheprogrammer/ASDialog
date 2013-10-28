'''
Functions for converting to and from intermediate values for communication with AppleScript.

All values passed back and forth between Python and AppleScript are done so through strings.
Many of the functions simply coerce values between a string and the native datatype. However,
some datatypes (such as dictionaries) must be serialized to an intermediate value and unserialized
by the other language.

For use with the AppleScript companion PYTranslate (http://github.com/pytranslate)
'''

from astranslate import bool
from astranslate import date
from astranslate import dict
from astranslate import list
from astranslate import number
from astranslate import string