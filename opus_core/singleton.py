#
# Opus software. Copyright (C) 1998-2007 University of Washington
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

class Singleton(object):
    
    _singletons = {}
    
    def __new__(cls, *args, **kwds):
        cls._is_new_instance = False
        if (not cls._singletons.has_key(cls)) or (kwds.has_key("new_instance") and kwds["new_instance"]):
            if cls._singletons.has_key(cls):
                del cls._singletons[cls]
            try:
                cls._singletons[cls] = object.__new__(cls)
            except TypeError:
                cls._singletons[cls] = dict.__new__(cls)
            cls._is_new_instance = True
        return cls._singletons[cls]
    
    def remove_singleton(self):
        self.remove_singleton_for_class(self.__class__)
            
    def is_new_instance(self):
        return self._is_new_instance
    
    def remove_singleton_for_class(self, klass):
        if self.has_singleton_for_class(klass):
            del self._singletons[klass]
            
    def remove_all_singletons(self):
        for klass in self._singletons.keys():
            self.remove_singleton_for_class(klass)
            
    def has_singleton_for_class(self, klass):
        return klass in self._singletons


from unittest import TestCase, main

class TestSingleton(TestCase):
    def test_singleton(self):
        """Also tests Singleton.has_singleton_for_class()."""
        class singleton_class_for_this_test(Singleton):
            pass
        
        # The only singleton should be Singleton itself.
        self.assertEqual(len(Singleton()._singletons), 1)
        self.assert_(Singleton().has_singleton_for_class(Singleton))
        self.assert_(not Singleton().has_singleton_for_class(singleton_class_for_this_test))
        
        # Create another singleton.
        singleton_class_for_this_test()
        
        # Both singletons should be in Singleton.
        self.assertEqual(len(Singleton()._singletons), 2)
        self.assert_(Singleton().has_singleton_for_class(singleton_class_for_this_test))
        
        # Can we remove a singleton?
        Singleton().remove_singleton_for_class(singleton_class_for_this_test)
        self.assertEqual(len(Singleton()._singletons), 1)
        self.assert_(Singleton().has_singleton_for_class(Singleton))
        self.assert_(not Singleton().has_singleton_for_class(singleton_class_for_this_test))        
        
if __name__ == '__main__':
    main()
