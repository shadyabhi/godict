#About the program

This GUI program uses unofficial Google Dictioary API to get the meanings.

 - Gets usage as verb, adjective, noun etc with examples.
 - Web definitions from various sources.

This is still under development & look & feel is going to improve & features will be added.

#How to use

The script looks for the word from the primary clipboard 
You can read about clipboards from here. (http://standards.freedesktop.org/clipboards-spec/clipboards-latest.txt)

Primary clipboard contains what's currently selected.

So, to use the program, you have to select a word in ANY application and 
execute the script godict.py using a shortcut (preferably)

In openbox, you can create a shortcut by adding 

    <keybind key="S-W-D">
    <action name="execute">
    <execute>/home/shadyabhi/github/godict/godict.py</execute>
    </action>
    </keybind>

to the .config/openbox/rc.xml
