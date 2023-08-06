"""
Overview
========

Used to insert tabs based on the type of file being edited.

Key-Commands
============

Namespace: spacing

Mode: INSERT
Event: <Tab>
Description: Insert a tab/space based on the programming file type.

"""

from os.path import splitext

class Tab(object):
    def __init__(self, area, tab_scheme, default_tab_size, default_char=' '):
        self.TAB_SIZE = None
        self.CHAR     = None

        def set_tab_scheme(event):
            ph, ext                  = splitext(area.filename.lower())
            self.TAB_SIZE, self.CHAR = tab_scheme.get(ext, (default_tab_size, default_char))

        area.install('spacing', (-1, '<FocusIn>', set_tab_scheme),
        ('INSERT', '<Tab>', lambda event: self.insert_tab(event.widget)))
    
    def insert_tab(self, area):
        area.edit_separator()
        area.insert('insert', self.CHAR * self.TAB_SIZE)
    
        return 'break'
    

install = Tab







