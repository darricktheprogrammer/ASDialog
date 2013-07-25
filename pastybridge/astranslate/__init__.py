'''
Functions for converting to and from intermediate values for communication with AppleScript.

All values passed back and forth between Python and AppleScript are done so through strings.
Many of the functions simply coerce values between a string and the native datatype. However,
some datatypes (such as dictionaries) must be serialized to an intermediate value and unserialized
by the other language.

For use with the AppleScript companion PYTranslate (http://github.com/pytranslate)
'''

import bool
import date
import dict
import list
import number
import string