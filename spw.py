#!/usr/bin/python
from gi.repository import Gtk, Gdk

from gi.repository import GObject
import gi
gi.require_version('WebKit', '3.0')
from gi.repository import WebKit
import threading;

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import Terminal256Formatter

lexer = get_lexer_by_name("javascript", stripall=True)
formatter = Terminal256Formatter(linenos=True, cssclass="source")

GObject.threads_init()


win = Gtk.Window()
def handle_keys(widget,event):
    print event
    modifiers=Gtk.accelerator_get_default_mod_mask()
    for mod in dir(Gdk.ModifierType): #just printing what the modifier is
        if (event.state&modifiers) == getattr(Gdk.ModifierType,mod): print(mod)
    print Gdk.keyval_name(event.keyval)

def set_title(webobj, frame, title):
    uri = web.get_uri();
    win.set_title(title + " -  " + uri)

def log_message(webobj, message, line, source_id):
    print message

class MyThread(threading.Thread):
    def __init__(self, web):
        super(MyThread, self).__init__()
        self.web = web
        self.quit = False

    def run_script(self, script):
        result = highlight(script, lexer, formatter)
        print(result)
        self.web.execute_script(script);
        return False

    def run(self):
        counter = 0
        while not self.quit:
            script = raw_input(":")
	    GObject.idle_add(self.run_script, script)

win.connect("delete-event", Gtk.main_quit)
win.connect('key-press-event', handle_keys)
web = WebKit.WebView()

web.open("http://www.google.com")
web.connect("title-changed", set_title)
web.connect("console-message", log_message)
win.add(web)
win.show_all()
t = MyThread(web)
t.start()

Gtk.main()

while True:
    script = raw_input(":")
