#!/usr/bin/python2

import gtk
import define
import pango
from HTMLParser import HTMLParser

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def sanitize(text):
    #text = text.replace("<em>", bold).replace("</em>", reset)
    text = text.replace("<em>", "").replace("</em>", "")
    text = text.replace("<b>", "").replace("</b>", "")
    text = HTMLParser.unescape.__func__(HTMLParser, text)
    return text


class GDiction:
    def __init__(self):
        #Creating the Window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Google Dictionary")
        self.window.set_border_width(10)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.connect("destroy", lambda w: gtk.main_quit())

        #VBox() contains all widgets
        self.vbox = gtk.VBox()
        self.window.add(self.vbox)

        #HBox() shows the word being searched
        self.hbox_word = gtk.HBox()
        self.label_word = gtk.Label()
        self.label_word.set_markup('<span foreground="blue" stretch="expanded">Word</span>')
        self.hbox_word.pack_start(self.label_word, False, True, 10)
        self.entry_word = gtk.Entry()
        self.hbox_word.pack_start(self.entry_word, True, True, 0)
        self.vbox.pack_start(self.hbox_word, True, True, 5)

        #A horizontal Separator
        separator = gtk.HSeparator()
        self.vbox.pack_start(separator, True, True, 10)

        #This gtk.TextView has the multi-line text which is to be sent
        self.textview_meaning = gtk.TextView()
        self.textview_meaning.set_size_request(600,400)
               
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        sw.add(self.textview_meaning)
        
        self.vbox.pack_start(sw, True, True, 10) 

        self.set_meaning_in_textview()


    def callback_clip(self,clipboard, text, data):
        if text is None:
            self.entry_word.set_text("NO TEXT SELECTED")
        else:
            means = define.get_meaning(text)
            self.entry_word.set_text(text)
           
            text_buffer = self.textview_meaning.get_buffer()
            #Creating tag
            heading_tag = text_buffer.create_tag( "h", size_points=16, weight=pango.WEIGHT_BOLD)
            italics_tag = text_buffer.create_tag( "i", style=pango.STYLE_ITALIC)
            ex_tag = text_buffer.create_tag( "colored", foreground="#FFFF00", background="#FFFFFF")
            color1_tag = text_buffer.create_tag( "colored1", foreground="#060E68", background="#CFD3FC")
            color2_tag = text_buffer.create_tag( "colored2", foreground="#344633", background="#EAF8C3")
                
            position = text_buffer.get_end_iter()
            for sec in means['primaries'].keys():
                meanings = means['primaries'][sec]
                text_buffer.insert_with_tags(position, "\n" + sec , heading_tag)
                position = text_buffer.get_end_iter()
                text_buffer.insert_with_tags(position, "\n---------------")
                for index, m in enumerate(meanings):
                    position = text_buffer.get_end_iter()
                    text_buffer.insert_with_tags(position, "\n" + str(index+1) + ".\t"+ sanitize(m[0]), color1_tag)
                    try:
                        for index, e in enumerate(m[1]): 
                            position = text_buffer.get_end_iter()
                            text_buffer.insert_with_tags(position, "\n" + "\t\t" + str(index + 1) + ". "  + sanitize(e), ex_tag, color2_tag)
                    except: pass
            
            position = text_buffer.get_end_iter()
            text_buffer.insert_with_tags(position, "\nWeb Definitions", heading_tag)
            text_buffer.insert_with_tags(text_buffer.get_end_iter(), "\n---------------")
            for index, defs in enumerate(means['webDefinitions']):
                position = text_buffer.get_end_iter()
                text_buffer.insert_with_tags(position, "\n" + str(index+1) + ".\t" + sanitize(defs) + "\n", color1_tag)
            
    def set_meaning_in_textview(self):
        clip = gtk.Clipboard(display=gtk.gdk.display_get_default(), selection="PRIMARY")
        clip.request_text(self.callback_clip)


    def main(self):
        self.window.show_all()
        gtk.main()

my_app = GDiction()
my_app.main()
