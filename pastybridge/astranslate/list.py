'''Convert list values back and forth between Applescript and Python.'''


def to_applescript(pyList):
	'''Delimit a list into a string value which the AppleScript library will be able to parse.'''
	pyStr = "|".join(str(item) for item in pyList)
	return "{" + pyStr + "}"

def to_python(asList):
	'''Parse a string passed in from AppleScript through the PYTranslate module'''
	level = 0
	pyList = []
	charCount = len(asList) - 1
	
	for i, c in enumerate(asList):
		if (level == 1) and ((c == "|") or (i == charCount)):
			end = i 
			pyList.append("".join(asList[start:end]))
			start = i + 1
		elif (c == "{"):
			if (level == 0):
				start = i + 1
			level = level + 1
		elif (c == "}"):
			level = level - 1
			
	return pyList