# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

class Singleton(object):
    
    _singletons = {}
    
    def __new__(cls, *args, **kwds):
        cls._is_new_instance = False
        if (cls not in cls._singletons) or ("new_instance" in kwds and kwds["new_instance"]):
            if cls in cls._singletons:
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
        for klass in list(self._singletons.keys()):
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
        self.assertTrue(Singleton().has_singleton_for_class(Singleton))
        self.assertTrue(not Singleton().has_singleton_for_class(singleton_class_for_this_test))
        
        # Create another singleton.
        singleton_class_for_this_test()
        
        # Both singletons should be in Singleton.
        self.assertEqual(len(Singleton()._singletons), 2)
        self.assertTrue(Singleton().has_singleton_for_class(singleton_class_for_this_test))
        
        # Can we remove a singleton?
        Singleton().remove_singleton_for_class(singleton_class_for_this_test)
        self.assertEqual(len(Singleton()._singletons), 1)
        self.assertTrue(Singleton().has_singleton_for_class(Singleton))
        self.assertTrue(not Singleton().has_singleton_for_class(singleton_class_for_this_test))        
        
if __name__ == '__main__':
    main()
