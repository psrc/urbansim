# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.logger import logger

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

    logger.log_error(traceback.format_exc())
    fExc_plain = fExc
    fExc = fExc.replace('\t','   ').replace('\n','<br>').replace(' ', '&nbsp;')
    errorinfo = ('''<qt>%s</qt>
                 '''%(fExc))    
    if plainText:
        return fExc_plain
    else:
        return errorinfo
