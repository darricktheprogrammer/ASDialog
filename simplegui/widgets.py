'''
Custom widget classes

All custom widgets are subclassed from their tk equivalent, unless otherwise noted (i.e. StyledButton = tk.Button + styling).
These classes are mostly built to allow for styling for each operating system.
'''
	
import Tkinter as tk

import common
import config


class StyledWindow(tk.Tk):
	'''Subclass of tk root object (Tk()) with added styling.'''
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.configure(background=config.BG_COLOR)

class StyledButton(tk.Button):
	'''Subclass of tk Button object with added styling.'''
	def __init__(self, *args, **kwargs):
		tk.Button.__init__(self, *args, **kwargs)
		self.configure(highlightbackground=config.BG_COLOR)
	
class StyledCheckbox(tk.Checkbutton):
	'''Subclass of tk Checkbutton object with added styling.'''
	def __init__(self, *args, **kwargs):
		tk.Checkbutton.__init__(self, *args, **kwargs)
		self.configure(bg=config.BG_COLOR)
		
class StyledFrame(tk.Frame):
	'''Subclass of tk Frame object with added styling.'''
	def __init__(self, *args, **kwargs):
		tk.Frame.__init__(self, *args, **kwargs)
		self.configure(bg=config.BG_COLOR)
		
class StyledDropdown(tk.OptionMenu):
	'''Subclass of tk OptionMenu object with added styling.'''
	def __init__(self, *args, **kwargs):
		tk.OptionMenu.__init__(self, *args, **kwargs)
		self.configure(bg=config.BG_COLOR)
		
class StyledInput(tk.Entry):
	'''Subclass of tk Entry object with added styling.'''
	def __init__(self, *args, **kwargs):
		tk.Entry.__init__(self, *args, **kwargs)		
		self.configure(highlightbackground=config.BG_COLOR)
		
class StyledLabel(tk.Label):
	'''Subclass of tk Label object with added styling.'''
	def __init__(self, *args, **kwargs):
		tk.Label.__init__(self, *args, **kwargs)
		self.configure(bg=config.BG_COLOR)
			
class StyledRadioButton(tk.Radiobutton):
	'''Subclass of tk Radiobutton object with added styling.'''
	def __init__(self, *args, **kwargs):
		tk.Radiobutton.__init__(self, *args, **kwargs)
		self.configure(bg=config.BG_COLOR)


class SimpleBooleanVar(tk.BooleanVar):
	'''Stores a boolean value instead of the Tkinter default of 0 or 1.'''
	def __init__(self, *args, **kwargs):
		tk.BooleanVar.__init__(self, *args, **kwargs)
	
	def get(self):
		return tk.BooleanVar.get(self) in ('1', True)



class SimpleRadioGroup(StyledFrame):
	'''
	Abstracts away the need to create a variable, assign it to multiple buttons,
	and manage the selection/deselection of each of the buttons.
	
	Kwargs:
		buttons (List[strings]): Possible values of the button group
		defaultButton String: The initial value (and selected button) of the group.
	Returns:
		SimpleRadioGroup Object
	'''
	def __init__(self, parent, buttons=[], defaultButton='', *args, **kwargs):
		StyledFrame.__init__(self, parent, *args, **kwargs)

		self._radiovalue = common.get_value_variable(buttons)
		self.add_buttons(buttons=buttons, defaultButton=defaultButton)

	# TODO: This should be made private
	def add_buttons(self, buttons=[], defaultButton=''):
		if defaultButton == '':
			defaultButton = buttons[0]

		for buttonName in buttons:
			button = StyledRadioButton(self, text=buttonName, variable=self._radiovalue, value=buttonName)
			button.pack(anchor=tk.W)
			if buttonName == defaultButton:
				button.select()
	
	def get(self):
		'''Overrides and abstracts the tk variable .get() function'''
		return self._radiovalue.get()