# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.logger import logger
import traceback

def formatExceptionInfo(custom_message = 'Unexpected error', maxTBlevel=5, plainText=False, log=True):
#    cla, exc, trbk = sys.exc_info()
    
#    excTb = traceback.format_tb(trbk, maxTBlevel)
#    excName = cla.__name__
#    try:
#        excArgs = exc.__dict__["args"]
#    except KeyError:
#        excArgs = "<no args>"
            
#    errorinfo = (excName, excArgs, excTb)

    format_message_and_error = lambda m, e: ('%s\n%s' % (m, e))  

    if log:
        logger.log_error(format_message_and_error(custom_message, traceback.format_exc()))

    fExc = format_message_and_error(custom_message, traceback.format_exc(limit=maxTBlevel))
    
    if plainText:
        return fExc
    else:
        fExc = fExc.replace('\t','   ').replace('\n','<br>').replace(' ', '&nbsp;')
        errorinfo = ('''<qt>%s</qt>
                     '''%(fExc))
        return errorinfo

def formatPlainTextExceptionInfo(*args, **kwargs):
    return formatExceptionInfo(*args, plainText=True, **kwargs)

def formatPlainTextExceptionInfoWithoutLog(*args, **kwargs):
    return formatPlainTextExceptionInfo(*args, log=False, **kwargs)

from opus_core.tests import opus_unittest
class ExceptionFormatterTests(opus_unittest.OpusTestCase):
    def test_formatPlainTextExceptionInfoRaisesErrorIfPlaintextIsGiven(self):
        self.assertRaises(Exception, formatPlainTextExceptionInfo, 'Message', 3, True)
        self.assertRaises(Exception, formatPlainTextExceptionInfo, 'Message', maxTBlevel=3, plainText=True)
        self.assertRaises(Exception, formatPlainTextExceptionInfoWithoutLog, 'Message', log=True)
        formatPlainTextExceptionInfo('Message', 3)
        formatPlainTextExceptionInfo('Message', maxTBlevel=3)
        formatPlainTextExceptionInfoWithoutLog('Message')

