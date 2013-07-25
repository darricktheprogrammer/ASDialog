from Tkinter import StringVar, DoubleVar, IntVar
from types import StringType, FloatType, IntType, BooleanType


def get_value_variable(values):
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