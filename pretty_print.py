#!/usr/bin/python2

import define
import sys
import httplib
import xml.dom.minidom
from HTMLParser import HTMLParser


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

means = define.get_meaning(sys.argv[1])
bold = "\033[1m"
reset = "\033[0;0m"


def sanitize(text):
    #text = text.replace("<em>", bold).replace("</em>", reset)
    text = text.replace("<em>", bcolors.OKGREEN).replace("</em>", bcolors.ENDC)
    text = HTMLParser.unescape.__func__(HTMLParser, text)
    return text

if means is not None:
    #Short Summary
    for sec in means['primaries'].keys():
        meanings = means['primaries'][sec]
        print sanitize(sec), "\n---------------"
        for meaning in meanings:
            print "\n\t", sanitize(meaning[0])
            try:
                for txt in meaning[1]:
                    print "\t\t--", sanitize(txt)
            except:
                pass

    #Web Definitions
    print "\nWeb Definitions", "\n---------------"
    for defs in means['webDefinitions']:
        defs.replace("<em>", bold).replace("</em>", reset)
        print "\t", sanitize(defs)
else:
    print "Word not found. These are he suggestions"
    data = """
    <spellrequest textalreadyclipped="0" ignoredups="0" ignoredigits="1" ignoreallcaps="1">
    <text> %s </text>
    </spellrequest>
    """
    word_to_spell = sys.argv[1]

    con = httplib.HTTPSConnection("www.google.com")
    con.request("POST", "/tbproxy/spell?lang=en", data % word_to_spell)
    response = con.getresponse()

    dom = xml.dom.minidom.parseString(response.read())
    dom_data = dom.getElementsByTagName('spellresult')[0]

    for child_node in dom_data.childNodes:
        result = child_node.firstChild.data.split()
        print sanitize(result)
