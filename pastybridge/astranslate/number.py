'''Convert a number value back and forth between Applescript and Python.'''

import exceptions



def to_applescript(num):
	'''
	Convert a Python number to a format that can be passed to Applescript.
	
	A number doesn't need coerced to print to stdout, but it's best to be thorough and explicit.
	'''
	return num

def to_python(num):
	'''
	Convert a string passed in from AppleScript to a Python number.
	
	http://stackoverflow.com/questions/379906/python-parse-string-to-float-or-int | Javier
	'''
	try:
		return int(num)
	except exceptions.ValueError:
		return float(num)