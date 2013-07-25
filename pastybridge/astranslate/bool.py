'''Convert boolean values back and forth between Applescript and Python'''


def to_applescript(b):
	'''Convert a Python boolean to a string to be passed back to AppleScript'''
	return str(b)

def to_python(b):
	'''Convert an AppleScript boolean string value into a Python Boolean'''
	return b.lower() in ("true", "yes", "1")