#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 


def formatExceptionInfo(custom_message = 'Unexpected error', maxTBlevel=5, plainText=False):
    import traceback

#    cla, exc, trbk = sys.exc_info()
    
#    excTb = traceback.format_tb(trbk, maxTBlevel)
    fExc = traceback.format_exc(limit=maxTBlevel)
    
#    excName = cla.__name__
#    try:
#        excArgs = exc.__dict__["args"]
#    except KeyError:
#        excArgs = "<no args>"
            
#    errorinfo = (excName, excArgs, excTb)

    print traceback.format_exc()
    fExc_plain = fExc
    fExc = fExc.replace('\t','   ').replace('\n','<br>').replace(' ', '&nbsp;')
    errorinfo = ('''<qt>%s<br><br>Details:<br><br><small>%s</small></qt>
                 '''%(custom_message, fExc))    
    if plainText:
        return fExc_plain
    else:
        return errorinfo
