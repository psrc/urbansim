# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

import time
import sys
from StringIO import StringIO
from unittest import TestResult, _WritelnDecorator, _strclass

from opus_core.logger import logger

    
def _get_centered_string(input_string, width):
    if len(input_string) < width:
        diff = width - len(input_string)
        margin_len = int(diff/2)
        margin = ' ' * margin_len
        input_string = '%s%s' % (margin, input_string)
    return input_string
    
def get_test_method_name(test):   
    # str(test) returns the method name followed by a space then the class name in parens
    return str(test).split(' ')[0]
 
class _OpusTextTestResult(TestResult):
    """A test result class that can print formatted text results to a stream.

    Used by OpusTextTestRunner.
    """
    sep_len = 80
    separator1 = '=' * sep_len
    separator2 = '-' * sep_len
    separator3 = '\xa6' * sep_len
    separator4 = '#' * sep_len
    separator5 = '\xa4' * sep_len
    
    ok_string = '%s( OK )%s' % ('-' * int((sep_len-6)/2), '-' * int((sep_len-6)/2))
    err_string = '%s( ERROR! )%s' % ('#' * int((sep_len-10)/2), '#' * int((sep_len-10)/2))
    fail_string = '%s( FAILURE! )%s' % ('#' * int((sep_len-12)/2), '#' * int((sep_len-12)/2))

    def __init__(self, stream, descriptions, verbosity):
        TestResult.__init__(self)
        self.stream = stream
        self.showAll = verbosity > 1
        self.dots = verbosity == 1
        self.descriptions = descriptions

    def getDescription(self, test):
        if self.descriptions:
            return test.shortDescription() or str(test)
        else:
            return str(test)

    def startTest(self, test):
        TestResult.startTest(self, test)
        if self.showAll:
            self.stream.writeln()
            self.stream.writeln()
            self.stream.writeln(self.separator1)
            
            methodName = logger._do_hide_error_and_warning_words(get_test_method_name(test))
            methodClass = logger._do_hide_error_and_warning_words(_strclass(test.__class__))
            
            self.stream.writeln(_get_centered_string(methodClass, self.sep_len))
            self.stream.writeln(_get_centered_string(methodName, self.sep_len))
            
            self.stream.writeln(self.separator1)

    def addSuccess(self, test):
        TestResult.addSuccess(self, test)
        if self.showAll:
            self.stream.writeln(self.ok_string)
        elif self.dots:
            self.stream.write('.')

    def addError(self, test, err):
        TestResult.addError(self, test, err)
        if self.showAll:
            self.stream.writeln(self.err_string)
        elif self.dots:
            self.stream.write('E')

    def addFailure(self, test, err):
        TestResult.addFailure(self, test, err)
        if self.showAll:
            self.stream.writeln(self.fail_string)
        elif self.dots:
            self.stream.write('F')

    def printErrors(self):
        if self.dots or self.showAll:
            self.stream.writeln()
        self.printErrorList('ERROR', self.errors)
        self.printErrorList('FAIL', self.failures)

    def printErrorList(self, flavour, errors):
        for test, err in errors:
            self.stream.writeln()
            self.stream.writeln()
            self.stream.writeln(self.separator4)
            self.stream.writeln("%s: %s" % (flavour,self.getDescription(test)))
            self.stream.writeln(self.separator5)
            self.stream.writeln()
            self.stream.writeln("%s" % err)
            self.stream.writeln(self.separator5)

class OpusTestRunner:
    """A test runner class that displays results in a nicely formatted textual 
    form.

    It prints out the names of tests as they are run, errors as they
    occur, and a summary of the results at the end of the test run.
    """
    def __init__(self, package, stream=sys.stderr, descriptions=False, verbosity=2):
        self.package = package
        self.stream = _WritelnDecorator(stream)
        self.descriptions = descriptions
        self.verbosity = verbosity

    def _makeResult(self):
        return _OpusTextTestResult(self.stream, self.descriptions, self.verbosity)

    def run(self, test):
        "Run the given test case or test suite."
        result = self._makeResult()
        startTime = time.time()
        test(result)
        stopTime = time.time()
        timeTaken = stopTime - startTime
        result.printErrors()
        
        self.stream.writeln()
        self.stream.writeln()
        
        if not result.wasSuccessful():
            self.stream.writeln(result.separator4)
        else:
            self.stream.writeln(result.separator3)
            
        self.stream.writeln()
        
        run = result.testsRun
        test_string = ("%d test%s (%.3fs)" 
            % (run, run != 1 and "s" or "", timeTaken))
        
        test_string = _get_centered_string(test_string, result.sep_len)

        package_name_msg = "'%s' Opus package" % self.package
        self.stream.writeln(_get_centered_string(package_name_msg, result.sep_len))
        self.stream.writeln(test_string)
        
        self.stream.writeln()

        if not result.wasSuccessful():
            failed, errored = map(len, (result.failures, result.errors))
            status_string = "(failures=%d, errors=%d)" % (failed, errored)
            
            status_string = _get_centered_string(status_string, result.sep_len)
            
            self.stream.writeln(_get_centered_string('RED LIGHT!', result.sep_len))
            self.stream.writeln(status_string)
            
        else:
            self.stream.writeln(_get_centered_string("ALL GREEN", result.sep_len))
            self.stream.writeln(_get_centered_string("Everything seems A-OK", result.sep_len))
            
        self.stream.writeln()
        
        if not result.wasSuccessful():
            self.stream.writeln(result.separator4)
        else:
            self.stream.writeln(result.separator3)
            
        self.stream.writeln()
        return result

from xml.dom.minidom import getDOMImplementation

class _OpusXMLTestResult(TestResult):
    """A test result class that can print formatted text results to a stream.

    Used by TextTestRunner.
    """

    def __init__(self, xml, descriptions, verbosity):
        TestResult.__init__(self)
        self.xml = xml
        self.showAll = verbosity > 1
        self.dots = verbosity == 1
        self.descriptions = descriptions
        self._testsuites = {}
        self._testsuite_xml = None
        self._testcase_xml = None

    def getDescription(self, test):
        if self.descriptions:
            return test.shortDescription() or str(test)
        else:
            return str(test)

    def startTest(self, test):
        TestResult.startTest(self, test)
        methodName = get_test_method_name(test)
        methodClass = _strclass(test.__class__)
        if methodClass not in self._testsuites:
            self._testsuite = self.xml.createElement('testsuite')
            self._testsuite.setAttribute('name', '%s' % methodClass)
            self._testsuites[methodClass] = self._testsuite
            self.xml.documentElement.appendChild(self._testsuite)
        else:
            self._testsuite = self._testsuites[methodClass]
        self._testcase_xml = self.xml.createElement('testcase')
        self._testcase_xml.setAttribute('name', '%s' % methodName)
        self._startTime = time.time()
    
    def stopTest(self, test):
        self._testcase_xml.setAttribute('time', '%.3f' % (time.time() - self._startTime))
        self._testsuite.appendChild(self._testcase_xml)

    def addSuccess(self, test):
        pass

    def addError(self, test, err):
        TestResult.addError(self, test, err)
        exctype, value, dummy_tb = err
        error_xml = self.xml.createElement('error')
        error_xml.setAttribute('type', '%s' % exctype)
        message_xml = self.xml.createTextNode('%s' % value)
        error_xml.appendChild(message_xml)
        self._testcase_xml.appendChild(error_xml)

    def addFailure(self, test, err):
        TestResult.addFailure(self, test, err)
        exctype, value, dummy_tb = err
        error_xml = self.xml.createElement('failure')
        error_xml.setAttribute('type', '%s' % exctype)
        message_xml = self.xml.createTextNode('%s' % value)
        error_xml.appendChild(message_xml)
        self._testcase_xml.appendChild(error_xml)

    def printErrors(self):
        pass

    def printErrorList(self, flavour, errors):
        pass
    
class OpusXMLTestRunner:
    """A test runner class that displays results in a nicely formatted textual 
    form.

    It prints out the names of tests as they are run, errors as they
    occur, and a summary of the results at the end of the test run.
    """
    def __init__(self, package, stream=sys.stderr, descriptions=False, verbosity=2):
        self.package = package
        self.stream = _WritelnDecorator(stream)
        self.descriptions = descriptions
        self.verbosity = verbosity

    def run(self, test):
        std_out = sys.stdout
        std_err = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        "Run the given test case or test suite."
        result_xml = getDOMImplementation().createDocument(None, 'testsuites', None)
        result = _OpusXMLTestResult(result_xml, self.descriptions, self.verbosity)
        startTime = time.time()
        test(result)
        stopTime = time.time()
        timeTaken = stopTime - startTime
        result.printErrors()
        
        run = result.testsRun
        
        failed, errored = map(len, (result.failures, result.errors))
        top_element = result_xml.documentElement
        top_element.setAttribute('errors', '%d' % errored)
        top_element.setAttribute('failures', '%d' % failed)
        top_element.setAttribute('tests', '%d' % run)
        top_element.setAttribute('time', '%.3f' % timeTaken)
        stream_xml = result_xml.createElement('system-out')
        stream_text_xml = result_xml.createTextNode('%s' % sys.stdout.getvalue())
        stream_xml.appendChild(stream_text_xml)
        top_element.appendChild(stream_xml)
        stream_xml = result_xml.createElement('system-err')
        stream_text_xml = result_xml.createTextNode('%s' % sys.stderr.getvalue())
        stream_xml.appendChild(stream_text_xml)
        top_element.appendChild(stream_xml)
        self.stream.write(result_xml.toprettyxml())
        sys.stdout = std_out
        sys.stderr = std_err
        return result
