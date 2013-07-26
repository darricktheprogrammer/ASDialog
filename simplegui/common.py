from Tkinter import StringVar, DoubleVar, IntVar
from types import StringType, FloatType, IntType, BooleanType


def get_value_variable(values):
	'''
	Gets the type of variable needed for Tkinter widgets.
	
	Will return the lowest common denominator variable for a value or list of values.
	For instance, if you have a list with both Strings and Integers, simplegui cannot
	return an IntVar. If the user choose a String, there will be an error.
	
	Args:
		values (Mixed): The value(s) where you want the lowest common denominator variable type.

	Returns:
		Tkinter Variable
	'''
	if not isinstance(values, list):
		values = [values]

	valueTypes = [type(value) for value in values]
	
	if StringType in valueTypes:
		return StringVar()
	elif FloatType in valueTypes:
		return DoubleVar()
	elif IntType in valueTypes:
		return IntVar()
	elif BooleanType in valueTypes:
		return SimpleBooleanVar()
	else:
		return StringVar()