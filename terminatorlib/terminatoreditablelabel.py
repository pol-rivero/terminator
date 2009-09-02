#!/usr/bin/env python
# vim: tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#
# Copyright (c) 2009, Emmanuel Bretelle <chantra@debuntu.org>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 2 only.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor
#    , Boston, MA  02110-1301  USA

# pylint: disable-msg=W0212
''' Editable Label class'''
import gtk

class TerminatorEditableLabel( gtk.EventBox ):
    '''
    An eventbox that partialy emulate a gtk.Label
    On double-click, the label is editable, entering an empty will revert back to automatic text
    '''
    _label = None
    _ebox = None
    _autotext = None
    _custom = None
    _entry = None
    _entry_handler_id = []
    def __init__(self, text = ""):
        ''' Class initialiser'''
        gtk.EventBox.__init__(self) 
        self._label = gtk.Label(text)
        self._custom = False
        self.set_visible_window (False)
        self.add (self._label)  
        self.connect ("button-press-event", self._on_click_text)

    def set_angle(self, angle ):
        '''set angle of the label'''
        self._label.set_angle( angle )
 
    def set_text( self, text, force=False):
        '''set the text of the label'''
        self._autotext = text
        if not self._custom or force:
            self._label.set_text(text) 

    def get_text( self ):
        '''get the text from the label'''
        return self._label.get_text()

    def _on_click_text(self, widget, event):
        '''event handling text edition'''
        if event.type == gtk.gdk._2BUTTON_PRESS :
            self.remove (self._label)
            self._entry = gtk.Entry ()
            self._entry.set_text (self._label.get_text ())
            self._entry.show ()
            self.add (self._entry)
            sig = self._entry.connect ("focus-out-event", self._entry_to_label)
            self._entry_handler_id.append(sig)
            sig = self._entry.connect ("activate", self._on_entry_activated)
            self._entry_handler_id.append(sig)
            sig = self._entry.connect ("key-press-event",
                                         self._on_entry_keypress)
            self._entry_handler_id.append(sig)
            self._entry.grab_focus ()
            return True
        # make pylint happy
        if 1 or widget or event:
            return False

    def _entry_to_label (self, widget, event):
        '''replace gtk.Entry by the gtk.Label'''
        if self._entry and self._entry in self.get_children():
            #disconnect signals to avoid segfault :s
            for sig in self._entry_handler_id:
                if self._entry.handler_is_connected(sig):
                    self._entry.disconnect(sig)
            self._entry_handler_id = []
            self.remove (self._entry)
            self.add (self._label)
            self._entry = None
            self.show_all ()
            return True
        #make pylint happy
        if 1 or widget or event:
            return False

    def _on_entry_activated (self, widget):
        '''get the text entered in gtk.Entry'''
        entry = self._entry.get_text ()
        label = self._label.get_text ()
        if entry == '':
            self._custom = False
            self.set_text (self._autotext)
        elif entry != label:
            self._custom = True
            self._label.set_text (entry)
        self._entry_to_label (None, None)

        # make pylint happy
        if 1 or widget:
            return

    def _on_entry_keypress (self, widget, event):
        '''handle keypressed in gtk.Entry'''
        key = gtk.gdk.keyval_name (event.keyval)
        if key == 'Escape':
            self._entry_to_label (None, None)
        # make pylint happy
        if 1 or widget or event:
            return
