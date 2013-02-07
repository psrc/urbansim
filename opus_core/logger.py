# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
import re
import sys
import time
import traceback

from gc import collect
from opus_core.singleton import Singleton
from opus_core.strings import indent_text
from functools import wraps
from contextlib import contextmanager

# Current code supports portable memory logging with psutil Python package.
_can_get_memory_usage = False
try:
    import psutil
    _can_get_memory_usage = True
except ImportError:
    pass

class _Logger(Singleton):
    """
    A singleton class to log messages.
    Log messages are sent to the standard output, and optionally to
    a file, if one is specified in enable_file_logging().
    Use the global logger, not __init__, to get reference to this logger.
    Logs memory usage if memory logging is enabled.
    By default, memory logging is disabled.
    """
    
    def __init__(self, *args, **kwargs):
        if self.is_new_instance():
            self._reset_state(*args, **kwargs)
    
    def _reset_state(self, *args, **kwargs):
        self._number_errors = 0
        self._number_warnings = 0
        self._number_notes = 0
        self._block_stack = []
        self._current_level = 0
        self._has_indent = True
        self._start_block_msg = ""
        self._output_width = 80
        self._file_stack = None   
        self._file_stream = None
        self._show_exact_time = False
        self._warning_file_stack = None
        self._is_logging_memory = False
        self._last_end_block_result = None
        self._log_to_file = False
        self._verbose = True
        self.__std_out_enabled = True
        self._hide_error_and_warning_words = False
        self.set_tags()
        self.set_verbosity_level()
    
    def set_tags(self, tags=[]):
        self.tags = tags
        
    def set_verbosity_level(self, verbosity_level=3):
        self.verbosity_level=verbosity_level
        
    def disable_std_out(self):
        """ Switch off logger to standard output """
        self.__std_out_enabled = False
        
    def enable_std_out(self):
        """ Switch off logger to standard output """
        self.__std_out_enabled = True
        
    def be_quiet(self):
        """Switch off logger output.""" 
        self._verbose = False
        
    def talk(self):
        """Switch on logger output.""" 
        self._verbose = True
        
    def write(self, s):
        self._write(s)
        
    def _writeln(self, s=None):
        if self._hide_error_and_warning_words and (s is not None):
            s = self._do_hide_error_and_warning_words(s)
        if s:
            self._write(s)
        self._do_write('\n')
        
    def _write(self, s):
        """
        Writes this string with the appropriate level of indentation.
        """
        msg = indent_text(s, 4 * self._current_level) 
        if not self._has_indent:
            self._writeln()
        self._has_indent = True
        self._do_write(msg)
        
    def _do_writeln(self, msg):
        self._do_write(msg)
        self._do_write('\n')
        
    def _do_write(self, msg):
        if self._verbose:
            if self._file_stack:
                for file_dict in self._file_stack:     
                    file_dict['file_stream'].write(msg)
            if self.__std_out_enabled :
                sys.stdout.write(msg)
            self.flush()
        
    def flush(self):
        if self._file_stream: 
            self._file_stream.flush()
        sys.stdout.flush()

    def enable_file_logging(self, file_name, mode='a', verbose=True):
        """
        Write all logger messages to this file using the given mode.
        """
        from opus_core.store.sftp_flt_storage import redirect_sftp_url_to_local_tempdir
        local_file_name = redirect_sftp_url_to_local_tempdir(file_name)
        if local_file_name != file_name:
            file_name = local_file_name
            verbose = True #always prompt where the log file is
        
        if verbose:
            self.log_status('Logging to file: ' + os.path.join(os.getcwd(),file_name))
            
        self.log_to_file = True
        
        if self._file_stack is None:
            self._file_stack = []
                        
        file_stream = open(file_name,mode)
        self._file_stack.append({"file_name" : file_name,
                                 "file_stream" : file_stream,
                                 "file_mode" : mode})
        os.getcwd()
                
    def disable_all_file_logging(self):
        """ close all file streams"""
        if self._file_stack is not None:
            while(len(self._file_stack) > 0):
                self.disable_file_logging()
        
    def disable_file_logging(self, filename=None):
        """
            Pop the last file name from the stack to stop writting on it. Close the file
        """
        if self._file_stack is not None  and len(self._file_stack) > 0:

            if filename is None:
                file_dict = self._file_stack.pop()
            else:
                filenames = map(lambda x: x['file_name'],self._file_stack )
                index = filenames.index(filename)
                file_dict = self._file_stack.pop(index)
            
            self.log_status('Closing log file: ' 
                            + os.path.join(os.getcwd(),file_dict['file_name']))
      
            file_dict['file_stream'].close()
            if not self._file_stack:
                self._log_to_file = False
            if self._warning_file_stack:
                warning_files = map(lambda x: x['file_name'],self._warning_file_stack )
                if self._warning_file_name(file_dict['file_name']) in warning_files:
                    index = warning_files.index(self._warning_file_name(file_dict['file_name']))
                    file_dict = self._warning_file_stack.pop(index)
                    self.log_status('Closing warning log file: ' 
                            + os.path.join(os.getcwd(), file_dict['file_name']))
   
                    file_dict['file_stream'].close()
                    
    def _end_block(self, block_stack_item, verbose):                
        found = False
        for i in reversed(self._block_stack):
            if i is block_stack_item:
                found = True
                break
        
        if not found:
            self.log_warning('Too many end_block() calls, log block not found on block stack: %s' % str(block_stack_item))
            return
        
        while True:
            if i is self._block_stack[-1]:
                self.end_block(verbose=verbose)
                return
            self.log_warning('Too many start_block() calls, auto-closing log block')
            self.end_block(verbose=True)
        
    @contextmanager
    def block(self, name='Unnamed block', verbose=True, *args, **kwargs):
        """ 
        arguments directly map to 
        logger.start_block(name='Unnamed block', verbose=True, tags=[], verbosity_level=3) 
    
        Enable block as a context manager, e.g.
        with logger.block(name='new block'):
            do something
            logger.log_status('log stuff')
    
        """
        block_stack_item = self.start_block(name=name, verbose=verbose, *args, **kwargs)
        try:
            yield None
        finally:
            self._end_block(block_stack_item=block_stack_item, verbose=verbose)
    
    def start_block(self, name='Unnamed block', verbose=True, tags=[], verbosity_level=3):
        """
        Starts a logger 'block'.  If in verbose mode, prints the current datetime.
        All logger messages until the next call to end_block() will
        be indented to show that they are contained in this block.
        """
        start_memory = self._start_log_memory()
        if self._should_log(tags, verbosity_level):    
            if (verbose):
                self._start_block_msg = name + ": started on " + time.ctime()
            else:
                self._start_block_msg = name
            self._write(self._start_block_msg)
            self._current_level += 1
            self._has_indent = False
            
        start_time = time.time()
        block_stack_item = (name, start_time, start_memory, tags, verbosity_level, self._show_exact_time, self._is_logging_memory)
        self._block_stack.append(block_stack_item)
        return block_stack_item
        
    def end_block(self, verbose=True):
        """
        Ends this 'block' of logger.  This returns the indentation level
        to it's prior state, and writes the elapsed time and memory
        usage to the log.  Memory usage is in kilobytes, and is only
        computed if the operating system supports it.
        Returns dictionary containing values for the elapsed time 
        ('elapsed_time'), and (if recorded) the amount of memory at 
        the start of this block ('start_memory'), and at the end of 
        this block ('end_memory').
        
        If verbose=True, print a "completed" message, too.
        """
        name, start_time, start_memory, tags, verbosity_level, self._show_exact_time, self._is_logging_memory = self._block_stack.pop()
        end_time = time.time()
        end_memory = self._end_log_memory()
        elapsed_time = end_time - start_time
        if self._should_log(tags, verbosity_level):
            elapsed_time_as_string = self._convert_seconds_to_human_readable_string(elapsed_time)
            msg = elapsed_time_as_string
            if self._is_logging_memory:
                msg += ", total %s, up %s" % (self._convert_memory_to_human_readable_string(end_memory),
                                              self._convert_memory_to_human_readable_string(end_memory - start_memory))
            self._current_level -= 1
            if not self._has_indent:
                self._has_indent = True
                self._do_writeln(self._uniform_width_with_start_block_msg(msg))
            else:
                if verbose:
                    self._writeln(self._uniform_width(name + ": completed", msg))
                else:
                    self._writeln(name)
        self._last_end_block_result = {"elapsed_time":elapsed_time}
        if self._is_logging_memory:
            self._last_end_block_result.update({"start_memory": start_memory,
                                                "end_memory": end_memory})
        return self._last_end_block_result

    
    def get_values_from_last_block(self):
        """
        Return the results of the last end_block() call.
        """
        return self._last_end_block_result
            
    def _start_log_memory(self):
        """
        Start logging memory usage.
        Each call to this method starts a new 'memory logging block'.
        Calling _end_log_memory() ends the current memory logging block
        and returns the amount of memory used since the opening call
        to _start_log_memory()."""
        if self._is_logging_memory:
            collect()
            cur_mem = self.memory_info()
            return cur_mem
        return 0
        
    def _end_log_memory(self):
        """Return the start and end amount of memory used by this 
        'memory logging block'."""
        if self._is_logging_memory:
            collect()
            end_mem = self.memory_info()
            return end_mem
        return 0
        
    def memory_info(self):
        p = psutil.Process(os.getpid())
        meminfo = p.get_memory_info() #returns (resident set size, virtual memory size)
        if meminfo != None and len(meminfo) == 2:
            return meminfo[1]
        return 0
    
    def enable_memory_logging(self):
        """Log memory usage for each logger 'block', if memory logging is supported
        on this computer."""
        self._is_logging_memory = _can_get_memory_usage
        
    def can_get_memory_usage(self):
        return _can_get_memory_usage
        
    def disable_memory_logging(self):
        """Turn off memory logging for logger 'block's."""
        self._is_logging_memory = False
        
    def enable_exact_time(self):
        self._show_exact_time = True
        
    def disable_exact_time(self):
        self._show_exact_time = False
        
    def log_status(self, *what_to_log, **kwargs):
        """Log the status to the logging pipe(s). 
        The semantics for this function is like that of print
        where your can have variable arguments of any type and 
        they will be concatinated into a string seperated by spaces. """
        # cast all arguments to unicode and join them with a space
        tags = kwargs.get("tags", [])
        level = kwargs.get("verbosity_level", 3)
        if self._should_log(tags, level):
            message = ' '.join(map(unicode, what_to_log))   
            self._writeln(message)

    def log_debug(self, message='',  **kwargs):
        l = kwargs.get("verbosity_level", 4)
        kwargs["verbosity_level"] = l
        self.log_status(message, **kwargs)

    def log_error(self, message=''):
        message = "ERROR: " + str(message)
        self._writeln(message)
        self._number_errors += 1

    def log_note(self, message=''):
        message = "NOTE: " + str(message)
        self._writeln(message)
        self._number_notes += 1
        
    def log_stack_trace(self):
        """Print the stack trace.
        """
        self.log_status("========== begin stack trace ==========")
        type, value, tb = sys.exc_info()
        stack_dump = ''.join(traceback.format_exception(type, value, tb))
        self.log_status(stack_dump)
        self.log_status("========== end stack trace ==========")
        
    def log_warning(self, message='', tags=[], verbosity_level=1):
        if self._should_log(tags, verbosity_level):
            message = "WARNING: " + str(message)
            self._writeln(message)
        self._number_warnings += 1

        if self._log_to_file:
            if self._warning_file_stack is None:
                self._warning_file_stack == self._open_warning_file_streams()
            for file_dict in self._warning_file_stack:
                file_dict['file_stream'].write(message + '\n')

    def _do_hide_error_and_warning_words(self, message):
        words_to_hide = {
            'ERROR' : 'E R R O R',
            'Error' : 'E r r o r',
            'error' : 'e r r o r',
            'WARNING' : 'W A R N I N G',
            'Warning' : 'W a r n i n g',
            'warning' : 'w a r n i n g',
            'Fail' : 'F a i l',
            'fail' : 'f a i l',
        }
        for old, new in words_to_hide.iteritems():
            message = message.replace(old, new)
        return message
        
    def _should_log(self, tags, level):
        for tag in tags:
            if tag in self.tags:
                return True
        if level <= self.verbosity_level:
            return True   
        return False
        
    def _open_warning_file_streams(self):
        """ open one warning file per file in the self._file_stack and initialize the 
        self._warning_file_stack variable"""

        w_file_stack  = []
        for file_dir in self._file_stack:
            filename = self._warning_file_name(file_dir['file_name'])
            logger.log_status("opening %s\n" % filename)
            stream = open(filename,file_dir['file_mode'])
            w_file_stack.append({"file_name": filename,"file_stream":stream,"file_mode": file_dir['file_mode']})
        
        return w_file_stack
        
    def _warning_file_name(self,filename):
        return "%s.WARNINGS.log" % filename
    
    def _convert_seconds_to_human_readable_string(self, seconds):
        days = (int (seconds /(24*3600))) % 365
        hours = (int (seconds / 3600)) % 24
        minutes = (int (seconds / 60)) % 60
        seconds_rounded = round((seconds % 60), 1)
        s = str(seconds_rounded) + " sec"
        if minutes: 
            s = str(minutes) + " min, " + s
        if hours: 
            s = str(hours) + " hrs, " + s
        if days: 
            s = str(days) + " days, " + s 
        if self._show_exact_time:
            s += (" (%.3f sec)" % seconds)
        return s
        
    @staticmethod
    def _convert_memory_to_human_readable_string(memory):
        memory_kb = memory / 1024
        memory_mb = memory_kb / 1024.0
        memory_mb_rounded = round(memory_mb, 1)
        return '%s MB' % memory_mb_rounded
        
    def _uniform_width(self, lhs, rhs):
        num_dots = max(3,
                       (self._output_width - len(lhs) - len(rhs) - self._current_level*4))
        dots = '.' * num_dots
        return lhs + dots + rhs
        
    def _uniform_width_with_start_block_msg(self, rhs):
        dots = '.' * (self._output_width - len(rhs) - self._current_level*4 - len(self._start_block_msg))
        if not dots or len(dots) <= 1:            
            return "...." + rhs
        else:
            return dots + rhs
        
    def enable_hidden_error_and_warning_words(self):
        """Add internal spaces to the automatically generated 'ERROR' and 'WARNING', so that 
        automated processes checking the output for errors or warnings won't find these messages."""
        self._hide_error_and_warning_words = True

    def disable_hidden_error_and_warning_words(self):
        """Stop hidding automatically generated 'ERROR' and 'WARNING' text."""
        self._hide_error_and_warning_words = False

# so callers can say 'from opus_core.logger import logger'.
logger = _Logger()        

def block(name='Unnamed block', verbose=True, *args, **kwargs):
    """ 
    arguments directly map to 
    logger.start_block(name='Unnamed block', verbose=True, tags=[], verbosity_level=3) 

    Enable block as a context manager, e.g.
    with block(name='new block'):
        do something
        logger.log_status('log stuff')

    """
    return logger.block(name=name, verbose=verbose, *args, **kwargs)

def log_block(*decorator_args, **decorator_kwargs):
    """ 
    arguments directly map to 
    logger.start_block(name='Unnamed block', verbose=True, tags=[], verbosity_level=3) 

    Decorator providing block logging:
    @log_block()
    def my_func(x, y):
        print x + y

    my_func('a', 'b')
    #outputs: 
    my_func: started on Tue Apr 17 10:14:12 2012........0.0 sec
    ab
    """
    def factory(func):
        if not decorator_args and 'name' not in decorator_kwargs:
            decorator_kwargs['name'] = func.__name__
        @wraps(func)
        def decorator(*func_args, **func_kwargs):
            with block(*decorator_args, **decorator_kwargs):
                return func(*func_args, **func_kwargs)
        return decorator
    return factory

import copy
from opus_core.tests import opus_unittest

class LoggerTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.logger_state = copy.deepcopy(logger.__dict__)
        logger._reset_state()
        logger.enable_hidden_error_and_warning_words()

    def tearDown(self):
        logger.__dict__ = copy.deepcopy(self.logger_state)
        logger.disable_hidden_error_and_warning_words()

    def test_do_hide_unwanted_words(self):
        logger.enable_hidden_error_and_warning_words()
        logger.log_error('Word "ERROR" should have spaces between letters.')
        logger.disable_hidden_error_and_warning_words()
        
    def test_logging_stack_trace(self):
        try:
            raise Exception('This message should appear as an error in the log (with spaces in error)')
        except:
            logger.enable_hidden_error_and_warning_words()
            logger.log_stack_trace()
            logger.disable_hidden_error_and_warning_words()

    def test_logs(self):
        logger.disable_file_logging()
        logger.log_status('before first block')
        logger.start_block('A')
        logger.log_status('a status')
        logger.start_block('B')
        logger.log_warning('a w a r n i n g')
        logger.log_error('an e r r o r')
        logger.end_block()
        logger.log_status("still in block A")
        logger.end_block()
        logger.log_status('after last block')
        
    def test_timing(self):
        logger.start_block('Timing test')
        logger.enable_exact_time()
        self.assert_(logger._show_exact_time)
        logger.start_block('Timing test with exact time')
        time.sleep(1)
        logger.end_block()
        logger.end_block()
        self.assert_(not logger._show_exact_time)
        
    def test_memory_logging(self):
        logger.start_block('A')
        logger.enable_memory_logging()
        logger.start_block('B')
        logger.start_block('C')
        logger.end_block()
        v1 = logger.end_block() 
        self.assertEqual(v1, logger.get_values_from_last_block())
        logger.disable_memory_logging()
        v2 = logger.end_block() 
        self.assertEqual(v2, logger.get_values_from_last_block())
        if logger.can_get_memory_usage():
            self.assertNotEqual(v1.keys(), v2.keys())
        else:
            self.assertEqual(v1.keys(), v2.keys())
        
    def test_empty_block(self):
        logger.start_block("empty C")
        logger.start_block("empty D")
        logger.end_block()
        logger.end_block()

    def test_long_block_name(self):
        logger.start_block("block with looooooooooooooooooooooooooooooooong name")
        logger.end_block()
        
    def test_ending_non_existing_block(self):
        logger.start_block('A')
        logger.end_block()
        try:
            logger.end_block()
            self.fail("Did not fail when ending a non-existing block.")
        except IndexError:
            pass
        
    def test_multiply_messages_log(self):
        from numpy import array
        logger.log_status("my favorite number is", 21, "but my mom's is", 14)
        logger.log_status(array(xrange(5)), "and i can count to", 2.0/3.0, "on a bad day")
        

    def test_multi_line_msg(self):
        logger.log_note('a\nb')
        logger.start_block('block')
        logger.log_status('first line\nsecond line')
        logger.end_block()
        
    def test_switch_logger(self):
        logger.log_status('you should see this')
        logger.be_quiet()
        logger.log_status('you should not see this')
        logger.talk()
        logger.log_status('and this')
        
    def test_multiple_file_logging(self):
        file_name_a = 'delete_me_a.log'
        file_name_b = 'delete_me_b.log'

        logger.enable_file_logging(file_name_a)
        self.assert_(len(logger._file_stack) == 1 )              
        logger.log_status('status in a')
        logger.enable_file_logging(file_name_b)
        self.assert_(len(logger._file_stack) == 2)
        logger.log_status('in both')
        logger.disable_file_logging(file_name_b)
        self.assert_(len(logger._file_stack) == 1 )

        logger.log_status("only in a")
        logger.disable_file_logging(file_name_a)
        self.assert_(len(logger._file_stack) == 0 )
        self.assert_(file_name_a in os.listdir('.'))
        self.assert_(file_name_b in os.listdir('.'))  
        os.remove(file_name_a)
        os.remove(file_name_b)
        # check that each file has what it's supposed to have

    def test_block(self):
        with logger.block("block"):
            pass

    def test_block_too_many_start_block_calls(self):
        with logger.block("block"):
            logger.start_block("extra start")

    def test_block_too_many_end_block_calls(self):
        with logger.block("block"):
            logger.end_block()

if __name__ == '__main__':
    opus_unittest.main()
    
