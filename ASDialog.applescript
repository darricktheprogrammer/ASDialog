property translate : missing value


on NewDialog(msg, scriptPath)
	set translate to load script file (scriptPath & "pastybridge:pytranslate.scpt")
	copy my Dialog to x
	set x's message to msg
	x's set_path(scriptPath)
	return x
end NewDialog







script Dialog
	property _myPath : missing value --		(** Folder containing ASDialog. *)
	
	property message : missing value --			(** Message to the user explaining the dialog. *)
	property _return_types : {} --				(** List of classes defining how each value should be returned after its trip to python *)
	property _widgets : {} --					(** List of widgets that will be displayed (added to every time an add_*() routine is called). *)
	property _cancelbutton : "Cancel" --	(** Button that will stop the script if clicked. *)
	property _title : "" --						(** Window title of the dialog. *)
	
	
	
	
	(**
	 * Set the folder path which contains ASDialog.
	 *
	 * It is important ASDialog knows where it is. That is the only
	 * way it can call the python bindings.
	 *
	 * @param	String	The folder containing ASDialog.
	 * @return	void
	 *)
	on set_path(pth)
		set _myPath to pth
		return
	end set_path
	
	
	(**
	 * Adds a title to the dialog window.
	 *
	 * @param	String	The window title.
	 * @return	void
	 *)
	on add_title(title)
		set _title to title
		return
	end add_title
	
	
	(*
	Routines for adding widgets
	*)
	
	(**
	 * Adds custom buttons to the dialog.
	 *
	 * This is not mandatory. The default {Cancel, OK} buttons will
	 * be used if no buttons are specified.
	 *
	 * @param	List		Names of the buttons, in order from left to right.
	 * @param	String	The button that should be clicked when the user presses enter (can be null or empty string if a default button is not desired).
	 * @param	String	Stops the script (can be null or empty string if a cancel button is not desired).
	 * @return	Dialog	The dialog the buttons belong to.
	 *)
	on add_buttons(buttonList, okbutton, cancelbutton)
		set _cancelbutton to cancelbutton
		set vals to {�
			{"buttons", buttonList}, �
			{"okButton", okbutton}, �
			{"cancelButton", cancelbutton}}
		return _add_widget("buttons", vals)
	end add_buttons
	
	(**
	 * Adds a checkbox to the dialog.
	 *
	 * Unlike other widgets, the label for the checkbox will be on the right side of the window.
	 *
	 * @param	String	The text description for the checkbox.
	 * @param	Bool	Initial state of the checkbox.
	 * @return	Dialog	The dialog the checkbox belongs to.
	 *)
	on add_checkbox(label, checked)
		_cache_return_value(boolean)
		set vals to {�
			{"label", label}, �
			{"checked", checked}}
		return _add_widget("checkbox", vals)
	end add_checkbox
	
	(**
	 * Adds a dropdown list menu to the dialog (where only one option can be chosen).
	 *
	 * @param	{String+Number}	Possible values for the user to choose.
	 * @param	String				The text description for the dropdown.
	 * @param	String+Number		Initial value shown in the dropdown.
	 * @return	Dialog				The dialog the dropdown belongs to.
	 *)
	on add_dropdown(values, label, defaultValue)
		_cache_return_value(values)
		set vals to {�
			{"label", label}, �
			{"values", translate's list_to_python(values)}, �
			{"defaultValue", defaultValue}}
		return _add_widget("dropdown", vals)
	end add_dropdown
	
	
	(**
	 * Adds a text field for user input.
	 *
	 * @param	String	The text description for the text field.
	 * @param	String	Initial value shown in the text field.
	 * @return	Dialog	The dialog the dropdown belongs to.
	 *)
	on add_text_field(label, defaultValue)
		_cache_return_value(string)
		set vals to {�
			{"label", label}, �
			{"defaultValue", defaultValue}}
		return _add_widget("textField", vals)
	end add_text_field
	
	
	(**
	 * Adds a group of radio buttons to the dialog.
	 *
	 * @param	{String+Number}	Possible values for the user to choose.
	 * @param	String				The text description for the radio group.
	 * @param	String+Number		Initial chosen value.
	 * @return	Dialog				The dialog the radio buttons belong to.
	 *)
	on add_radio_buttons(buttonList, label, defaultButton)
		_cache_return_value(buttonList)
		set vals to {�
			{"label", label}, �
			{"choices", buttonList}, �
			{"defaultButton", defaultButton}}
		return _add_widget("radioButtons", vals)
	end add_radio_buttons
	
	
	(**
	 * Same as add_separator_with_label, but without adding a label.
	 *
	 * @return	Dialog	The dialog the radio buttons belong to.
	 *)
	on add_separator()
		return add_separator_with_label("")
	end add_separator
	
	
	(**
	 * Adds a separating line between elements.
	 *
	 * @param	String	The text description for the separator.
	 * @return	Dialog	The dialog the radio buttons belong to.
	 *)
	on add_separator_with_label(label)
		set vals to {�
			{"label", label}}
		return _add_widget("separator", vals)
	end add_separator_with_label
	
	
	
	(**
	 * Pops the dialog up to the user and returns the values the user chose in an Associative Array.
	 *
	 * Must be called after widgets have been added to the dialog, otherwise it won't do anything.
	 *
	 * @return	AssociativeArray
	 *)
	on display()
		set vals to do shell script _compile_shell_script()
		set returnedData to _unserialize(vals)
		if readKey("button returned") of returnedData is _cancelbutton then
			error number -128
		end if
		
		set values to readKey("values") of returnedData
		repeat with i from 1 to (count values)
			set item i of values to _convert_to_applescript(item i of values, item i of _return_types)
		end repeat
		return {buttonReturned:readKey("button returned") of returnedData, values:values}
	end display
	
	
	
	
	
	(**
	 * Create an AssociativeArray with widget properties and add to the list of widgets.
	 *
	 * @param	String	The type of widget (i.e.: buttons, separator, checkbox, �).
	 * @return	Dialog
	 *)
	on _add_widget(widgetType, widgetProperties)
		set array to translate's newAssociativeArray()
		set widgetProperties to {{"name", widgetType}} & widgetProperties
		repeat with i from 1 to (count widgetProperties)
			set {k, v} to {item 1, item 2} of item i of widgetProperties
			array's setKey(k, v)
		end repeat
		set end of _widgets to array
		return me
	end _add_widget
	
	
	(**
	 * Compiles the arguments together and creates the
	 * formatted shell command for calling the python bindings.
	 *
	 * @return	String
	 *)
	on _compile_shell_script()
		set args to _compile_args()
		set pieces to {"python", "-B", quoted form of POSIX path of (_myPath & "asdialog.py"), args}
		return my implode(pieces, space)
	end _compile_shell_script
	
	
	(**
	 * Compiles together all of the arguments to be sent to the python bindings,
	 * including serializing all of the widget arrays.
	 *
	 * @return	List
	 *)
	on _compile_args()
		set args to {quoted form of message, quoted form of _title}
		repeat with i from 1 to (count _widgets)
			set end of args to quoted form of (translate's array_to_python(item i of _widgets))
		end repeat
		return args
	end _compile_args
	
	
	(**
	 * Goes through and makes sure that all values have been unserialized.
	 *
	 * This should be implemented in AssociativeArray's unserialize instead.
	 *
	 * @param	String	Value returned from python.
	 * @return	AssociativeArray
	 *)
	on _unserialize(vals)
		set valueArray to translate's array_to_applescript(vals)
		set {keys, values} to valueArray's {getKeys(), getValues()}
		
		repeat with i from 1 to (count keys)
			set {k, v} to {item i of keys, item i of values}
			if v contains "|" then
				valueArray's setKey(k, translate's list_to_applescript(v))
			end if
		end repeat
		return valueArray
	end _unserialize
	
	
	
	
	
	(**
	 * Returns the lowest common denominator class for a value or list of values
	 *
	 * Given a list of values with the classes {real, real, integer} this routine will return 'number'
	 * Given a list of values with the classes {string, string, boolean} it will return 'string.'
	 * A string can not always be coerced into a boolean, but a boolean can always be coerced into a string
	 *
	 * @param	Mixed	The value or list of values to which you want to find the lowest common denominator class
	 * @return	Class
	 *)
	on _get_class(values)
		if class of values is not list then set values to {values}
		
		set classList to {}
		repeat with i from 1 to (count values)
			set c to class of item i of values
			if c is string then
				--Exit early for lowest common denominator 
				return string
			else
				set end of classList to c
			end if
		end repeat
		
		if (number is in classList) or (real is in classList) or (integer is in classList) then
			return number
		else if boolean is in classList then
			return boolean
		else
			return string
		end if
	end _get_class
	
	
	(**
	 * Helper routine to coerce values returned from python back into their AppleScript equivalent.
	 *
	 * @param	String	The returned python value to convert.
	 * @param	Class	The class that the value should be coerced to.
	 * @return	Mixed
	 *)
	on _convert_to_applescript(val, valType)
		if valType is string then
			return translate's string_to_applescript(val)
			
		else if valType is number then
			return translate's number_to_applescript(val)
			
		else if valType is boolean then
			return translate's bool_to_applescript(val)
			
		else if valType is date then
			return translate's date_to_applescript(val)
		end if
	end _convert_to_applescript
	
	
	(**
	 * Helper routine to coerce values into python readable strings.
	 *
	 * @param	Mixed	The value to convert into a python value
	 * @return	String
	 *)
	on _convert_for_python(val)
		if class of val is number then
			return translate's number_to_python(val)
		else if class of val is date then
			return translate's date_to_python(val)
		else if class of val is boolean then
			return translate's bool_to_python(val)
		else
			return translate's string_to_python(val)
		end if
	end _convert_for_python
	
	
	(**
	 * Saves the class of a value in the _return_types property.
	 *
	 * If given a class, it will directly cache that value. If given a value,
	 * it will use _get_class() to determine the class to use.
	 *
	 * @param	Class+Mixed
	 * @return	void
	 *)
	on _cache_return_value(val)
		if class of val is not class then
			set val to _get_class(val)
		end if
		set end of _return_types to val
		return
	end _cache_return_value
end script






--Sub-routine to join a list into a string
--------------------------------------------------------------------------------
on implode(theList, theDelim)
	set AppleScript's text item delimiters to theDelim
	set theText to theList as text
	set AppleScript's text item delimiters to ""
	return theText
end implode