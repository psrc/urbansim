#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

try:
    from enthought.traits import Class, Long, Str, Int
    from enthought.traits.ui import Handler
    from enthought.traits.ui.menu import Action, CloseAction

except ImportError:
    pass

else:    
    from opus_core.tools.command.command import Command

    
    class CommandGui(Handler):
        _command_class = Class ### TODO: How to ensure that it is a subclass of Command?
        _command_instance = None
        
        _execute_button = Action(name='Execute', action='_do_execute')
        _buttons = [_execute_button, CloseAction]
        
        _traits_that_are_not_command_parameters = [
            'trait_added',
            '_command_class',
            '_command_instance',
            'trait_modified',
            ]
        
        def __init__(self, command_class):
            self._command_class = command_class
            self._command_instance = None
        
        def load(self):
            pass
            
        def save(self):
            pass
        
        def execute(self):
            command = self._get_command_instance()
            
#            if not command.is_valid():
#                command.get_validation_information()
                
            command.execute()
        
        def _get_command_instance(self):
            if self._command_instance is not None:
                return self._command_instance
            
            traits_to_use = {}
            for trait in self.trait_names():
                if trait not in self._traits_that_are_not_command_parameters:
                    traits_to_use[trait] = eval('self.%s' % trait)
            
            self._command_instance = self._command_class(**traits_to_use)
            return self._command_instance
            
        def _do_execute(self, info):
            self.execute()            
            self._on_close(info)
            
        def _anytrait_changed(self, changed_trait):
            """
            Resets the saved command instance if a trait has changed. We'll be
            needing a new one.
            """
            # If it was _command_instance that changed 
            #     (e.g. in _get_command_instance), don't unset it right after!
            if changed_trait != '_command_instance':
                self._command_instance = None
            
    
    from opus_core.tests import opus_unittest
    
    
    class TestCommandGui(opus_unittest.OpusTestCase):
        def setUp(self):        
            self.my_command_gui = CommandGui(self.__mock_command)
            
        def tearDown(self):
            pass
        
        def test_returns_an_instance_of_the_command_when_get_command_instance_is_called(self):
            instance = self.my_command_gui._get_command_instance()
            self.assert_(isinstance(instance, self.__mock_command))
            
        def test_returns_same_instance_of_the_command_when_get_command_instance_is_called_more_than_once(self):
            first_instance = self.my_command_gui._get_command_instance()
            second_instance = self.my_command_gui._get_command_instance()
            self.assert_(first_instance is second_instance)
        
        def test_executes_command_when_execute_is_called(self):
            self.my_command_gui.execute()
            command_instance = self.my_command_gui._get_command_instance()
            self.assert_(command_instance.last_executed)
            
#        def test_gets_validation_information_when_execute_is_called_with_invalid_parameters(self):
#            command_instance = self.my_command_gui._get_command_instance()
#            command_instance.return_value_for_is_valid = False
#            self.my_command_gui.execute()
#            
#            command_instance2 = self.my_command_gui._get_command_instance()
#            self.assert_(command_instance is command_instance2)
#            self.assert_(command_instance2.last_validation_information_retrieved)
    
        def test_executes_command_with_correct_parameters_when_execute_is_called(self):
            self.my_command_gui.add_trait('a_string', Str)
            self.my_command_gui.add_trait('an_int', Int)
            
            self.my_command_gui.a_string = 'hello, there'
            self.my_command_gui.an_int = 100
            
            self.my_command_gui.execute()
            
            expected_args = ()
            expected_kwargs = {
                'a_string':'hello, there', 
                'an_int':100
                }
            
            command_instance = self.my_command_gui._get_command_instance()
            self.assertEqual(command_instance.last_args, expected_args)
            self.assertEqual(command_instance.last_kwargs, expected_kwargs)
            
        def test_executes_command_with_correct_parameters_when_execute_is_called_triangulate(self):
            self.my_command_gui.add_trait('a_long', Long)
            self.my_command_gui.add_trait('an_int', Int)
            
            self.my_command_gui.an_int = 100
            self.my_command_gui.a_long = 3L
            
            self.my_command_gui.execute()
            
            expected_args = ()
            expected_kwargs = {
                'a_long':3L, 
                'an_int':100
                }
            
            command_instance = self.my_command_gui._get_command_instance()
            self.assertEqual(command_instance.last_args, expected_args)
            self.assertEqual(command_instance.last_kwargs, expected_kwargs)
            
        def test_executes_command_with_correct_parameters_when_execute_is_called2(self):
            # Take 1
            self.my_command_gui.add_trait('a_string', Str)
            self.my_command_gui.add_trait('an_int', Int)
            
            self.my_command_gui.a_string = 'hello, there'
            self.my_command_gui.an_int = 100
            
            self.my_command_gui.execute()
            
            expected_args = ()
            expected_kwargs = {
                'a_string':'hello, there', 
                'an_int':100
                }
            
            command_instance = self.my_command_gui._get_command_instance()
            self.assertEqual(command_instance.last_args, expected_args)
            self.assertEqual(command_instance.last_kwargs, expected_kwargs)
            
            # Take 2
            del self.my_command_gui.a_string
            self.my_command_gui.add_trait('a_long', Long)
            self.my_command_gui.a_long = 3L
            
            self.my_command_gui.execute()
                    
            expected_args = ()
            expected_kwargs = {
                'a_long':3L, 
                'an_int':100
                }
            
            command_instance = self.my_command_gui._get_command_instance()
            self.assertEqual(command_instance.last_args, expected_args)
            self.assertEqual(command_instance.last_kwargs, expected_kwargs)
            
        class __mock_command(Command):
            def __init__(self, *args, **kwargs):
                self.last_executed = False
                self.last_is_validated = False
                self.last_validation_information_retrieved = False
                self.return_value_for_is_valid = True
                self.last_args = args
                self.last_kwargs = kwargs
                
            def is_valid(self):
                self.last_is_validated = True
                return self.return_value_for_is_valid
                
            def get_validation_information(self):
                self.last_validation_information_retrieved = True
                return None
                
            def execute(self):
                self.last_executed = True
            
    
    if __name__ == '__main__':
        opus_unittest.main()
