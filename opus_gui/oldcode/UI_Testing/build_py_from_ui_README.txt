How to turn .ui files into python code, command line example:

pyuic4 -o opusMain_testing.py opusMain_testing.ui -x

How to turn the resource (.qrc, this holds references to the icons I used) files into python code:

pyrcc4 -o opusMain_rc.py opusMain.qrc

Also see pyuic4.bat in the Python25 directory (at least on windows) for more info on how this works.  I think that points to pyuic.py in PyQt4 in site-packages. 
