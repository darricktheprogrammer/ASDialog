'''
Convert date values back and forth between Applescript and Python.

Use the Applescript string value of a date as an intermediate value for
passing back and forth. This is easily coerced into a date by both languages
as long as the standard is followed.

Date string format: "Thursday, January 1, 1970 12:00:00 AM"
'''

from datetime import datetime
from datetime import timedelta

AS_DATE_FORMAT = "%A, %B %d, %Y %I:%M:%S %p"



def to_applescript(pyDate):
	'''Convert a Python date object in a string that AppleScript can coerce into its own date object.'''
	return pyDate.strftime(AS_DATE_FORMAT)

def to_python(asDate):
	'''Convert an AppleScript date string to a Python date object.'''
	return datetime.strptime(asDate, AS_DATE_FORMAT)