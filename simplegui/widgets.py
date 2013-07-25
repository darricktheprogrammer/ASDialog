import Tkinter as tk

import common
import config


class StyledWindow(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.configure(background=config.BG_COLOR)

class StyledButton(tk.Button):
	def __init__(self, *args, **kwargs):
		tk.Button.__init__(self, *args, **kwargs)
		self.configure(highlightbackground=config.BG_COLOR)
	
class StyledCheckbox(tk.Checkbutton):
	def __init__(self, *args, **kwargs):
		tk.Checkbutton.__init__(self, *args, **kwargs)
		self.configure(bg=config.BG_COLOR)
		
class StyledFrame(tk.Frame):
	def __init__(self, *args, **kwargs):
		tk.Frame.__init__(self, *args, **kwargs)
		self.configure(bg=config.BG_COLOR)
		
class StyledDropdown(tk.OptionMenu):
	def __init__(self, *args, **kwargs):
		tk.OptionMenu.__init__(self, *args, **kwargs)
		self.configure(bg=config.BG_COLOR)
		
class StyledInput(tk.Entry):
	def __init__(self, *args, **kwargs):
		tk.Entry.__init__(self, *args, **kwargs)		
		self.configure(highlightbackground=config.BG_COLOR)
		
class StyledLabel(tk.Label):
		def __init__(self, *args, **kwargs):
			tk.Label.__init__(self, *args, **kwargs)
			self.configure(bg=config.BG_COLOR)
			
class StyledRadioButton(tk.Radiobutton):
	def __init__(self, *args, **kwargs):
		tk.Radiobutton.__init__(self, *args, **kwargs)
		self.configure(bg=config.BG_COLOR)


class SimpleBooleanVar(tk.BooleanVar):
	def __init__(self, *args, **kwargs):
		tk.BooleanVar.__init__(self, *args, **kwargs)
	
	def get(self):
		return tk.BooleanVar.get(self) in ('1', True)



class SimpleRadioGroup(StyledFrame):
	def __init__(self, parent, buttons=[], defaultButton='', *args, **kwargs):
		StyledFrame.__init__(self, parent, *args, **kwargs)

		self._radiovalue = common.get_value_variable(buttons)
		self.add_buttons(buttons=buttons, defaultButton=defaultButton)
			
	def add_buttons(self, buttons=[], defaultButton=''):
		if defaultButton == '':
			defaultButton = buttons[0]

		for buttonName in buttons:
			button = StyledRadioButton(self, text=buttonName, variable=self._radiovalue, value=buttonName)
			button.pack(anchor=tk.W)
			if buttonName == defaultButton:
				button.select()
	
	def get(self):
		return self._radiovalue.get()
			


			
			