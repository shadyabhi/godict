#!/usr/bin/python2

import define
import sys
import httplib
import xml.dom.minidom


means = define.get_meaning(sys.argv[1])

if means is not None:
    #Short Summary
    for sec in means['primaries'].keys():
        meanings = means['primaries'][sec]
        print sec, "\n---------------"
        for m in meanings:
            print "\n\t", m[0]
            try: 
                for e in m[1]: print "\t\t--",e
            except: pass

    #Web Definitions
    print "\nWeb Definitions","\n---------------"
    for defs in means['webDefinitions']:
        print "\t",defs
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
        print result
