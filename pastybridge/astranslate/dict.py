'''
Convert dictionary values back and forth between Applescript and Python.

The Associative Array is a custom data type inside the ASTranslate/PYTranslate modules.
On the Python side, it is simply a delimited string that Python can create from a dictionary or parse into one.
'''

import exceptions
import types

import list


class invalidArrayString(Exception):
	'''Exception used to define an error in parsing an Applescript string into a dictionary'''
	pass



def to_applescript(pyDict):
	'''Convert a dictionary into an Associative Array for passing back to AppleScript'''
	pairs = []
	for k, v in pyDict.items():
		if (isinstance(v, types.ListType)):
			v = list.to_applescript(v)
		pairs.append("<" + k + "=" + v + ">")

	return "".join(pairs)

def to_python(asArray):
	'''Convert an Associative Array passed in from AppleScript into a Python dictionary'''
	if (len(asArray) < 3) or ("<" not in asArray) or (">" not in asArray):
		raise invalidArrayString("'" + str(asArray) + "' is not a valid Array")

	dict = {}
	asArray = str(asArray[1:len(asArray)-1])
	pairs = asArray.split("><")
	for pair in pairs:
		k, v = pair.split("=")
		dict[k] = v
	return dict