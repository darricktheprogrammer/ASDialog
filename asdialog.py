#!"/usr/bin/python"
'''Applescript wrapper which allows access to the simplegui python module.'''

import sys
from Foundation import NSAppleScript
from datetime import datetime

from pastybridge import astranslate as translate
from simplegui import simplegui as gui


# 
# Global values for debugging
# 
debugging = False
debug_msg = "Hello World"
debug_title = "Window Title"
# debug_widgets = ["<name=textField><label=Enter some text>", "<name=radioButtons><choices={1|2|3}><label=radio choice>", "<name=buttons><buttons={b1|b2}>"]
debug_widgets = ['<name=buttons><buttons={Cancel|OK}><okButton=OK><cancelButton=Cancel>', '<name=checkbox><label=A checkbox><checked=False>', '<name=checkbox><label=Another checkbox><checked=True>']







def bring_dialog_to_front():
	s = NSAppleScript.alloc().initWithSource_("tell app \"Python\" to activate")
	s.executeAndReturnError_(None)


def add_widget(d, widget):
	widgetName = widget.pop('name')

	if widgetName == "buttons":
		bList = widget.pop('buttons')
		d.add_buttons(bList, **widget)
	elif widgetName == "checkbox":
		label = widget.pop('label')
		widget['checked'] = translate.bool.to_python(widget['checked'])
		d.add_checkbox(label, **widget)
	else:
		dialogRoutines = {
							"dropdown":     d.add_dropdown,
							"textField":    d.add_text_field,
							"radioButtons": d.add_radio_buttons,
							"separator":    d.add_separator
							}
		dialogRoutines[widgetName](**widget)
	return d



def unpack_list_values(dict):
	for k, v in dict.iteritems():
		if "|" in v:
			dict[k] = translate.list.to_python(v)
	return dict


def main():
	msg, title, widgets = ((debug_msg, debug_title, debug_widgets) if debugging
							else (sys.argv[1], sys.argv[2], sys.argv[3:]))

	for i, w in enumerate(widgets):
		widgetProperties = translate.dict.to_python(w)
		widgets[i] = unpack_list_values(widgetProperties)

	d = gui.Dialog(msg, title=title)	
	for w in widgets:
		d = add_widget(d, w)
	
	bring_dialog_to_front()	
	print translate.dict.to_applescript(d.display())




if __name__ == '__main__':
	main() 
