import os
import win32com.client
import win32api
#from SendKeys import SendKeys

maploc = "c:\\temp\\djfksljafkls.mxd"
scriptloc = "c:\\temp\\AddMapSurrounds.vbs"

(filepath, filename) = os.path.split(maploc)
retVal = os.startfile(maploc)
wtitle = filename.join(" - ArcMap - ArcInfo")

shell = win32com.client.Dispatch("WScript.Shell")
win32api.Sleep(6000)
shell.appactivate(wtitle)

shell.SendKeys("%{F11}") #send Alt-F11 to open Visual Basic Editor
shell.appactivate("Microsoft Visual Basic - ".join(filename)) # switch focus to Visual Basic Editor
win32api.Sleep(1000)
shell.SendKeys("%{F}{I}") #send Alt-F, I to import script file
#shell.SendKeys("^{M}") #send ctrl-M to import script file
win32api.Sleep(500)
shell.SendKeys(scriptloc) #send script file location
win32api.Sleep(500)
shell.SendKeys("%{O}") #select open
win32api.Sleep(500)
shell.SendKeys("{F5}") #run VBA script
win32api.Sleep(500)
shell.SendKeys("%{R}") #run macro

