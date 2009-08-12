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


#SendKeys("""{LWIN}rNotepad.exe{SPACE}"%(filename)s"{ENTER}{PAUSE 1}""" 
#         % {'filename': filename.replace('~','{~}')}, with_spaces=True)
#
#SendKeys.SendKeys("""
#    {LWIN}
#    {PAUSE .25}
#    r
#    Notepad.exe{ENTER}
#    {PAUSE 1}
#    Hello{SPACE}World!
#    {PAUSE 1}
#    %{F4}
#    n
#""")

#- Use FindWindow to get the handle of the application you want to control;
#- Send a message to the given window to bring it to the top;
#- Control the application by means of keystrokes. I dont remember the 
#funcion key, but I think that it should be SendKeys or something similar. 
#There are examples on how to make it work in VB; you can use the same idea 
#from Python (I assume that pythoncom/win32 area already exposing this 
#function).

#Dim HWND As Long
#HWND = FindWindow(vbNullString, "Untitled - Notepad")

#    Dim lHandle As Long
#    lHandle = FindWindow(vbNullString, "Untitled - Notepad")
#    Call ShowWindow(lHandle, 3)
#    Call SetForegroundWindow(lHandle)
