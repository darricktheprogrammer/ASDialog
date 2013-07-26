'''
Main module of the simplegui package.

Labels are optional (but encouraged) text descriptions for each widget, and
are located on the left side of the Dialog window. Widgets are located on
the right side of the window.

Widgets will be added top-down in the order the add_*() methods are called.
	
Usage:
    Create a new dialog, add any widgets you need, then display the dialog.
    The dialog will return a dictionary with the values the user chose, along
    with the button that was pressed (button will be None if the window
    is closed without a button selection).
    
Example:
    >>> d = simplegui.simplegui.Dialog()
    >>> d.add_dropdown(label="Select a value:",
                       values=['val1', 'val2', 'val3'],
                       defaultValue='val1')
    >>> d.add_text_field(label="Enter a value:")
    >>> d.display()
    {'values': [val1, val2], 'button returned': 'Ok'}   
'''

import Tkinter as tk

import common
import config
import widgets


class Dialog():
	'''
	A window with methods for abstracting the creation of simple user input.
	'''
	def __init__(self, message, title=''):
		'''
		Initialization code for the Dialog
		
		Args:
			message (String): Message/Directions to the user.
		Kwargs:
			title (String): Text to show in the title bar of the window.
		Returns:
			Dialog object
		'''
		self._root = self._get_root_window(title)
		self._labelwidth = 0
		self._widgetwidth = 0
		self._returnValues = {'values': [], 'button returned': None}

		self._variables = []
		self._widgets = []
		self._labels = []
		self._buttons = None
		self._nextrow = 1
		self._message = message
		
	
	#
	# Public methods
	# Most are methods for adding widgets to the dialog.
	#
	def display(self):
		'''
		Call after populating with widgets to display the window to the user and receive their input.
		
		Returns:
			Dictionary
		'''
		messagewidth = self._labelwidth + self._widgetwidth + (config.PADDING_CENTER * 2) + (config.PADDING_OUTER * 2)
		
		if self._buttons == None:
			self.add_buttons()
		self._pack_buttons()
		self._add_message(self._message, messagewidth)
		self._resize_widgets()
		self._resize_labels()
		self._center_window(self._root)
		self._root.mainloop()
		return self._returnValues


	# This caches the button properties, but does not add them. Buttons are added
	# at the end, during the display() method.
	def add_buttons(self, buttons=['Cancel', 'Ok'], okButton='Ok', cancelButton='Cancel'):
		'''
        Adds custom buttons to the Dialog.
        
        It is not mandatory to call this method. If the standard ['Cancel', 'Ok']
        buttons are sufficient, they will be added automatically.

        Kwargs:
            buttons (List): List of buttons, in Left->Right order.
            okButton (Mixed): Button that is returned when the user
                              presses Return/Enter
            cancelButton (Mixed): Button that is returned when the user
                                  presses a cancelling key combination
                                  (such as Cmd+. on Mac)
        Returns:
            None
		'''
		self._buttons = {'buttons':      buttons,
						 'okbutton':     okButton,
						 'cancelbutton': cancelButton}
			
			
	def add_checkbox(self, label='', checked=False):
		'''
		Adds a boolean checkbox to the Dialog.

		Kwargs:
			label (String): Text description of the checkbox.
			checked (Bool): Initial state of the checkbox.
		Returns:
			None
		'''
		checkboxVal = widgets.SimpleBooleanVar()
		self._variables.append(checkboxVal)
		chbx = widgets.StyledCheckbox(self._root, text=label, variable=checkboxVal)
		self._pack_widget(chbx)
		chbx.configure(justify=tk.LEFT)
		if checked:
			chbx.select()


	def add_dropdown(self, label='', values=[], defaultValue=''):
		'''
		Adds a dropdown menu for the user to choice a single value.

		Kwargs:
			label (String): Text description of the checkbox.
			values (List): Values the user can choose from.
			defaultValue (Mixed): Initial state of the dropdown.
		Returns:
			None
		'''
		dropdownVal = common.get_value_variable(values)
		self._variables.append(dropdownVal)
		longestValue = max(str(values), key=len)
		dropdownVal.set(longestValue)

		dropdown = widgets.StyledDropdown(self._root, dropdownVal, *values)
		self._pack_widget(dropdown, labelText=label, fillColumn=True)
		dropdownVal.set(defaultValue)
		
		
	def add_text_field(self, label='', defaultValue=''):
		'''
		Adds a field to the Dialog where the user can type.

		Kwargs:
			label (String): Text description of the checkbox.
			defaultValue (String): Initial state of the dropdown.
		Returns:
			None
		'''
		fieldVal = tk.StringVar()
		fieldVal.set(defaultValue)
		self._variables.append(fieldVal)
		textField = widgets.StyledInput(self._root, textvariable=fieldVal)
		self._pack_widget(textField, labelText=label, fillColumn=True)
		
		
	def add_radio_buttons(self, choices=[], label='', defaultButton=''):
		'''
		Adds a linked group of radio buttons to the Dialog.

		Kwargs:
			buttons (List): Values the user can choose from.
			defaultValue (Mixed): Initially selected button.
		Returns:
			None
		'''
		radioGroup = widgets.SimpleRadioGroup(self._root, buttons=choices, defaultButton=defaultButton)
		self._variables.append(radioGroup)
		self._pack_widget(radioGroup, labelText=label)
		
		
	def add_separator(self, label=''):
		'''
		Adds a horizontal line between widgets.
		
		Separators do not return values. They are only used to visually separate
		groups of information. If you add a checkbox, separator, and text field
		to a Dialog, you will only receive two values from display(): that of 
		the checkbox and text field.

		Kwargs:
			label (String): Can be used as a text description for the group.
		Returns:
			None
		'''
		separator = widgets.StyledFrame()
		separator.configure(height=1, background=config.BG_SHADOW)
		self._pack_widget(separator, labelText=label, fillColumn=True)
		
		
	#
	# Private Methods
	#
	def _get_root_window(self, title):
		'''
		Creates a new instance of StyledWindow to use as the root node in the dialog.

		Args:
			title (String): The window title
		Returns:
			StyledWindow()
		'''
		win = widgets.StyledWindow()
		win.configure(padx=config.PADDING_OUTER, pady=config.PADDING_OUTER)
		win.title(title)
		win.resizable(0, 0)
		return win


	def _get_values(self, buttonClicked):
		'''
		Gathers the current widget values and destroys the window.

		Args:
			buttonClicked (String): The name of the button the user selected.
		Returns:
			None
		'''
		self._returnValues['button returned'] = buttonClicked
		for var in self._variables:
			try:
				self._returnValues['values'].append(var.get())
			except ValueError:
				self._returnValues['values'].append(None)
		self._root.destroy()
	
	
	def _pack_widget(self, widget, labelText='', fillColumn=False):
		'''
		Adds the widget to the Dialog.

		Args:
			widget (Widget): The widget to pack.
			labelText (String): Text description of the widget
			fillColumn (Bool): Should the widget expand across the entire column?
			                   Helpful to keep dropdowns and text fields uniform.
		Returns:
			None
		'''
		stickyType = tk.EW if fillColumn else tk.W
		widgetLabel = widgets.StyledLabel(self._root, text=labelText)
		widgetLabel.grid(column=0, row=self._nextrow, padx=(0, config.PADDING_CENTER), pady=(config.PADDING_TOP, config.PADDING_BOTTOM), sticky=tk.E)
		widgetLabel.configure(anchor=tk.E)
		widget.grid(column=1, row=self._nextrow, pady=(config.PADDING_TOP, config.PADDING_BOTTOM), sticky=stickyType)

		if widgetLabel.winfo_reqwidth() > self._labelwidth:
			self._labelwidth = widgetLabel.winfo_reqwidth()
		
		if widget.winfo_reqwidth() > self._widgetwidth:
			self._widgetwidth = widget.winfo_reqwidth()
			
		self._labels.append(widgetLabel)
		self._widgets.append(widget)
		self._nextrow += 1
		
		
	def _pack_buttons(self):
		'''
		Adds buttons to the Dialog.
		
		This exists as a separate method because buttons need to be added right
		before displaying, so they don't end up in the middle of the Dialog.

		Returns:
			None
		'''
		buttons = self._buttons['buttons']
		okButton = self._buttons['okbutton']
		cancelButton = self._buttons['cancelbutton']

		buttonFrame = widgets.StyledFrame(self._root)
		buttonFrame.grid(row=self._nextrow, columnspan=2, sticky=tk.SE, pady=(config.PADDING_BOTTOM, config.PADDING_TOP))

		for buttonName in reversed(buttons):
			button = widgets.StyledButton(buttonFrame, text=buttonName)
			button.configure(command=lambda bn=buttonName: self._get_values(bn))
			if buttonName == okButton:
				button.configure(default='active')
			button.pack(side=tk.RIGHT)

		if okButton is not None and okButton in buttons:
			self._root.bind('<Return>', lambda event, ok=okButton: self._get_values(ok))
			self._root.bind('<KP_Enter>', lambda event, ok=okButton: self._get_values(ok))
		if cancelButton is not None and cancelButton in buttons:
			self._root.bind('<Command-.>', lambda event, cancel=cancelButton: self._get_values(cancel))
			# TODO: Add cancelling key combinations for other systems.
		
		
	def _add_message(self, message, windowWidth):
		'''
		Adds the message to the top of the Dialog.
		
		This exists as a separate method because the message spans both columns
		of the dialog, and it is not known until display time how wide each column
		will be.
		
		Args:
			message (String): Message to be displayed to the user.
			windowWidth (Int): The entire width of the Dialog window
			
		Returns:
			None
		'''	
		messageWidth = windowWidth - (config.PADDING_OUTER * 2) - (config.PADDING_CENTER * 2)
		messageWidget = widgets.StyledLabel(self._root, text=message, justify=tk.LEFT, wraplength=messageWidth)
		messageWidget.grid(row=0, columnspan=2, pady=(config.PADDING_TOP, config.PADDING_BOTTOM + 10), sticky=tk.W)


	def _center_window(self, win):
		'''
		Centers the window on screen.
		
		from http://stackoverflow.com/a/10018670/2348587
		'''
		win.update_idletasks()
		frm_width = win.winfo_rootx() - win.winfo_x()
		win_width = win.winfo_width() + (frm_width*2)
		titlebar_height = win.winfo_rooty() - win.winfo_y()
		win_height = win.winfo_height() + (titlebar_height + frm_width)
		x = (win.winfo_screenwidth() / 2) - (win_width / 2)
		y = (win.winfo_screenheight() / 2) - (win_height / 2)
		geom = (win.winfo_width(), win.winfo_height(), x, y)
		win.geometry('{0}x{1}+{2}+{3}'.format(*geom))


	def _resize_widgets(self):
		'''Resizes all widgets to a uniform width.'''
		for widget in self._widgets:
			widget.configure(width=
							self._widgetwidth / len(self._widgets) - self._widgetwidth / len(self._widgets)
							)
	
	
	def _resize_labels(self):
		'''Resizes all labels to a uniform width.'''
		for label in self._labels:
			label.configure(width=
							self._labelwidth / len(self._labels) - self._labelwidth / len(self._labels)
							)