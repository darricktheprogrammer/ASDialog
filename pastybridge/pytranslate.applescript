(*
##########################################################################
#
# Functions for converting to and from intermediate values for communication with Python.
#
# All values passed back and forth between Python and AppleScript are done so through strings.
# Many of the functions simply coerce values between a string and the native datatype. However,
# some datatypes (such as lists) must be serialized to an intermediate value and unserialized
# by the other language.
#
# For use with the Python companion ASTranslate (http://github.com/astranslate)
#
##########################################################################
*)(*
Number
*)(**
 * Convert a Python input string into an AppleScript number
 *
 * @param	String	A number in string format
 * @return	Number
 *)on number_to_applescript(num)	return num as numberend number_to_applescript(**
 * Convert an AppleScript number into a string for passing to Python
 *
 * @param	Number
 * @return	String
 *)on number_to_python(num)	return num as stringend number_to_python(*
Boolean
*)(**
 * Convert a Python input string into an AppleScript boolean
 *
 * @param	String	A boolean in string format
 * @return	Bool
 *)on bool_to_applescript(bool)	return bool as booleanend bool_to_applescript(**
 * Convert an AppleScript boolean into a string for passing to Python
 *
 * @param	Bool
 * @return	String
 *)on bool_to_python(bool)	return titleCase(bool as string)end bool_to_python(*
List
*)(**
 * Parse a string passed in from Python through the ASTranslate module
 *
 * @param	String
 * @return	List
 *)on list_to_applescript(str)	set level to 0	set l to {}	set charCount to length of str		repeat with i from 1 to charCount		set c to character i of str				if (level is 1) and ((c is "|") or (i = charCount)) then			set endPos to i - 1			if endPos < startPos then				--Two pipes in a row equal an empty string				set end of l to ""			else				set end of l to (characters startPos thru endPos of str as string)			end if			set startPos to i + 1		else if (c is "{") then			if level is 0 then				set startPos to i + 1			end if			set level to level + 1		else if (c is "}") then			set level to level - 1		end if	end repeat	return lend list_to_applescript(**
 * Convert a list into a pipe-delimited string value which the Python library will be able to parse.
 *
 * @param	List
 * @return	String
 *)on list_to_python(asList)	set str to implode(asList, "|")	return "{" & str & "}"end list_to_python(*
Date
*)(**
 * Convert an AppleScript date object into a string for Python
 *
 * @param	Date
 * @return	String
 *)on date_to_applescript(d)	return d as stringend date_to_applescript(**
 * Convert a Python input string into an AppleScript date object
 * 
 * All formatting for dates are done in python, since there is a built-in module.
 *
 * @param	String	A date string in the format: "Thursday, January 1, 1970 12:00:00 AM"
 * @return	Date
 *)on date_to_python(d)	return date dend date_to_python(*
String
*)(**
 * Remove Unix quotes from a Python string
 *
 * @param	String
 * @return	String
 *)on string_to_applescript(pyString)	if pyString begins with "'" then		if ((count pyString) > 2) then			return (characters 2 thru -2 of pyString) as string		else			return ""		end if	end if	return pyStringend string_to_applescript(**
 * Add Unix quotes to an AppleScript string for Python
 *
 * @param	String
 * @return	String
 *)on string_to_python(str)	return quoted form of strend string_to_python(*
Dictionary/Associative Array
*)(**
 * Convert an Associative Array passed in from Python into an Associative Array.
 *
 * The Associative Array is a custom data type inside the ASTranslate/PYTranslate modules.
 *
 * @param	String	A string that has been serialized using the PAsty Bridge library
 * @return	AssociativeArray
 *)on array_to_applescript(str)	if str begins with "'" then		set str to translate_from_PYString(str)	end if	set array to newAssociativeArray()	array's unserialize(str)	return arrayend array_to_applescript(**
 * Convert an Associative Array to a string for passing into Python.
 *
 * The Associative Array is a custom data type inside the ASTranslate/PYTranslate modules.
 *
 * @param	AssociativeArray
 * @return	String
 *)on array_to_python(array)	return array's serialize()end array_to_python(** 
 * AssociativeArray Class
 *
 * A custom class, related to a Hash table (C/C++), Dictionary (Python), or Associative Array (php).
 * This class was created to deal with the limitation of not being able to build records dynamically
 * through variables, like you are able to do with Python Dictionaries.
 *)on newAssociativeArray()	script AssociativeArray		property _keys : {} --	(** List	Contains keys for the array *)		property _values : {} --	(** List	Contains values for the array *)						(**
		 * Adds a new key, or update an existing key in the array.
		 *
		 * 
		 * @param	Mixed	A key to search by later.
		 * @param	Mixed	Value linked to a key.
		 * @return	AssociativeArray
		 *)		on setKey(k, v)			set displayV to v			if class of v is list then				set displayV to my list_to_string(v, ", ")			end if						set keyIndex to _getKeyIndex(k)			if keyIndex is 0 then				_append(k, v)			else				set item keyIndex of _values to v			end if			return me		end setKey				(**
		 * Get the value of a given key.
		 *
		 * Will throw an error if the key is not found.
		 *
		 * @param	Mixed	The key to search by.
		 * @return	Mixed	The value associated with the key.
		 *)		on readKey(k)			set keyIndex to _getKeyIndex(k)			if keyIndex is 0 then				error "Key '" & k & "' not found"			end if			return item keyIndex of _values		end readKey				(**
		 * Returns a list of all keys in the array.
		 *
		 * @return	List
		 *)		on getKeys()			return _keys		end getKeys				(**
		 * Returns a list of all values in the array.
		 *
		 * @return	List
		 *)		on getValues()			return _values		end getValues				(**
		 * Converts all data in the array into a String for use in other programs.
		 *
		 * Each key/value pair is serialized in the format: "<k=v>"
		 * If the value is a list, it will be pipe delimited: "<k=v1|v2|v3>"
		 *
		 * @return	String
		 *)		on serialize()			set pairList to {}			repeat with i from 1 to (count _keys)				set k to item i of _keys				set v to item i of _values				if class of v is list then					set v to my list_to_string(v, "|")				end if				set end of pairList to "<" & k & "=" & v & ">"			end repeat			return pairList as string		end serialize				(**
		 * Dumps a string of serialized data into the targeted AssociativeArray.
		 *
		 * The array needs to be created first,
		 * then the routine can be called to insert data.
		 *
		 * @param	String
		 * @return	AssociativeArray
		 *)		on unserialize(str)			if ((count str) < 3) or str does not contain "<" or str does not contain ">" then				set errMsg to "Cannot create Associative Array from the string " & quoted form of str				error errMsg number -1001			end if						set str to items 2 thru -2 of str as string			set pairList to my explode(str, "><")			repeat with i from 1 to (count pairList)				set {k, v} to my explode(item i of pairList, "=")				setKey(k, v)			end repeat			return me		end unserialize				(**
		 * Adds a new key/value pair to the array.
		 *
		 * Used internally by setKey() for keys that do not already exist.
		 *
		 * @param	Mixed
		 * @param	Mixed
		 * @return	void
		 *)		on _append(k, v)			set end of _keys to k			set end of _values to v			return		end _append				(**
		 * Determines where the key is located in the list.
		 *
		 * Will return 0 if the key is not found.
		 *
		 * @param	Mixed	The key to find
		 * @return	Number
		 *)		on _getKeyIndex(k)			repeat with i from 1 to (count _keys)				if item i of _keys is k then					return i				end if			end repeat			return 0		end _getKeyIndex	end scriptend newAssociativeArray(*
##########################################################################
#
# Helper functions
#
##########################################################################
*)--Sub-routine to change the case of text to title case--------------------------------------------------------------------------------on titleCase(theText)	set allWords to my explode(theText, space)		set fixedWords to {}	repeat with i from 1 to (count allWords)		set currWord to item i of allWords		set thisWord to ""		repeat with j from 1 to (count currWord)			if j = 1 then				set thisWord to thisWord & my toUpper(item j of currWord)			else				set thisWord to thisWord & my toLower(item j of currWord)			end if		end repeat		set end of fixedWords to thisWord	end repeat	return my implode(fixedWords, space)end titleCase--Sub-routine to make text lowercase--------------------------------------------------------------------------------on toLower(theText)	set lowerLetters to "abcdefghijklmnopqrstuvwxyz"	set upperLetters to "ABCDEFGHIJKLMNOPQRSTUVWXYZ"		repeat with i from 1 to (count upperLetters)		set theText to my searchAndReplace(theText, item i of upperLetters, item i of lowerLetters)	end repeat	return theTextend toLower--Sub-routine to make text uppercase--------------------------------------------------------------------------------on toUpper(theText)	set lowerLetters to "abcdefghijklmnopqrstuvwxyz"	set upperLetters to "ABCDEFGHIJKLMNOPQRSTUVWXYZ" as Unicode text		repeat with i from 1 to (count lowerLetters)		set theText to my searchAndReplace(theText, item i of lowerLetters, item i of upperLetters)	end repeat	return theTextend toUpper--Sub-routine to search a string for text and replace it with new text--------------------------------------------------------------------------------on searchAndReplace(myString, oldText, newText)	set AppleScript's text item delimiters to oldText	set myList to text items of myString	set AppleScript's text item delimiters to newText	set myString to myList as string	set AppleScript's text item delimiters to ""	return myStringend searchAndReplace--Sub-routine to explode a string into a list--------------------------------------------------------------------------------on explode(theText, theDelim)	set AppleScript's text item delimiters to theDelim	set theList to text items of theText	set AppleScript's text item delimiters to ""	return theListend explode--Sub-routine to join a list into a string--------------------------------------------------------------------------------on implode(theList, theDelim)	set AppleScript's text item delimiters to theDelim	set theText to theList as text	set AppleScript's text item delimiters to ""	return theTextend implodeon list_to_string(l, delimiter)	return "{" & my implode(l, delimiter) & "}"end list_to_string