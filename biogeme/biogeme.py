# This file was created automatically by SWIG 1.3.29.
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.

from . import _biogeme
import new
new_instancemethod = new.instancemethod
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'PySwigObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static) or hasattr(self,name):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError(name)

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

import types
try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0
del types


class PySwigIterator(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, PySwigIterator, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, PySwigIterator, name)
    def __init__(self): raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __swig_destroy__ = _biogeme.delete_PySwigIterator
    __del__ = lambda self : None;
    def value(*args): return _biogeme.PySwigIterator_value(*args)
    def incr(*args): return _biogeme.PySwigIterator_incr(*args)
    def decr(*args): return _biogeme.PySwigIterator_decr(*args)
    def distance(*args): return _biogeme.PySwigIterator_distance(*args)
    def equal(*args): return _biogeme.PySwigIterator_equal(*args)
    def copy(*args): return _biogeme.PySwigIterator_copy(*args)
    def next(*args): return _biogeme.PySwigIterator_next(*args)
    def previous(*args): return _biogeme.PySwigIterator_previous(*args)
    def advance(*args): return _biogeme.PySwigIterator_advance(*args)
    def __eq__(*args): return _biogeme.PySwigIterator___eq__(*args)
    def __ne__(*args): return _biogeme.PySwigIterator___ne__(*args)
    def __iadd__(*args): return _biogeme.PySwigIterator___iadd__(*args)
    def __isub__(*args): return _biogeme.PySwigIterator___isub__(*args)
    def __add__(*args): return _biogeme.PySwigIterator___add__(*args)
    def __sub__(*args): return _biogeme.PySwigIterator___sub__(*args)
    def __iter__(self): return self
PySwigIterator_swigregister = _biogeme.PySwigIterator_swigregister
PySwigIterator_swigregister(PySwigIterator)

class vectorInt(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, vectorInt, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, vectorInt, name)
    __repr__ = _swig_repr
    def iterator(*args): return _biogeme.vectorInt_iterator(*args)
    def __iter__(self): return self.iterator()
    def __nonzero__(*args): return _biogeme.vectorInt___nonzero__(*args)
    def __len__(*args): return _biogeme.vectorInt___len__(*args)
    def pop(*args): return _biogeme.vectorInt_pop(*args)
    def __getslice__(*args): return _biogeme.vectorInt___getslice__(*args)
    def __setslice__(*args): return _biogeme.vectorInt___setslice__(*args)
    def __delslice__(*args): return _biogeme.vectorInt___delslice__(*args)
    def __delitem__(*args): return _biogeme.vectorInt___delitem__(*args)
    def __getitem__(*args): return _biogeme.vectorInt___getitem__(*args)
    def __setitem__(*args): return _biogeme.vectorInt___setitem__(*args)
    def append(*args): return _biogeme.vectorInt_append(*args)
    def empty(*args): return _biogeme.vectorInt_empty(*args)
    def size(*args): return _biogeme.vectorInt_size(*args)
    def clear(*args): return _biogeme.vectorInt_clear(*args)
    def swap(*args): return _biogeme.vectorInt_swap(*args)
    def get_allocator(*args): return _biogeme.vectorInt_get_allocator(*args)
    def begin(*args): return _biogeme.vectorInt_begin(*args)
    def end(*args): return _biogeme.vectorInt_end(*args)
    def rbegin(*args): return _biogeme.vectorInt_rbegin(*args)
    def rend(*args): return _biogeme.vectorInt_rend(*args)
    def pop_back(*args): return _biogeme.vectorInt_pop_back(*args)
    def erase(*args): return _biogeme.vectorInt_erase(*args)
    def __init__(self, *args): 
        this = _biogeme.new_vectorInt(*args)
        try: self.this.append(this)
        except: self.this = this
    def push_back(*args): return _biogeme.vectorInt_push_back(*args)
    def front(*args): return _biogeme.vectorInt_front(*args)
    def back(*args): return _biogeme.vectorInt_back(*args)
    def assign(*args): return _biogeme.vectorInt_assign(*args)
    def resize(*args): return _biogeme.vectorInt_resize(*args)
    def insert(*args): return _biogeme.vectorInt_insert(*args)
    def reserve(*args): return _biogeme.vectorInt_reserve(*args)
    def capacity(*args): return _biogeme.vectorInt_capacity(*args)
    __swig_destroy__ = _biogeme.delete_vectorInt
    __del__ = lambda self : None;
vectorInt_swigregister = _biogeme.vectorInt_swigregister
vectorInt_swigregister(vectorInt)

class vectorDouble(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, vectorDouble, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, vectorDouble, name)
    __repr__ = _swig_repr
    def iterator(*args): return _biogeme.vectorDouble_iterator(*args)
    def __iter__(self): return self.iterator()
    def __nonzero__(*args): return _biogeme.vectorDouble___nonzero__(*args)
    def __len__(*args): return _biogeme.vectorDouble___len__(*args)
    def pop(*args): return _biogeme.vectorDouble_pop(*args)
    def __getslice__(*args): return _biogeme.vectorDouble___getslice__(*args)
    def __setslice__(*args): return _biogeme.vectorDouble___setslice__(*args)
    def __delslice__(*args): return _biogeme.vectorDouble___delslice__(*args)
    def __delitem__(*args): return _biogeme.vectorDouble___delitem__(*args)
    def __getitem__(*args): return _biogeme.vectorDouble___getitem__(*args)
    def __setitem__(*args): return _biogeme.vectorDouble___setitem__(*args)
    def append(*args): return _biogeme.vectorDouble_append(*args)
    def empty(*args): return _biogeme.vectorDouble_empty(*args)
    def size(*args): return _biogeme.vectorDouble_size(*args)
    def clear(*args): return _biogeme.vectorDouble_clear(*args)
    def swap(*args): return _biogeme.vectorDouble_swap(*args)
    def get_allocator(*args): return _biogeme.vectorDouble_get_allocator(*args)
    def begin(*args): return _biogeme.vectorDouble_begin(*args)
    def end(*args): return _biogeme.vectorDouble_end(*args)
    def rbegin(*args): return _biogeme.vectorDouble_rbegin(*args)
    def rend(*args): return _biogeme.vectorDouble_rend(*args)
    def pop_back(*args): return _biogeme.vectorDouble_pop_back(*args)
    def erase(*args): return _biogeme.vectorDouble_erase(*args)
    def __init__(self, *args): 
        this = _biogeme.new_vectorDouble(*args)
        try: self.this.append(this)
        except: self.this = this
    def push_back(*args): return _biogeme.vectorDouble_push_back(*args)
    def front(*args): return _biogeme.vectorDouble_front(*args)
    def back(*args): return _biogeme.vectorDouble_back(*args)
    def assign(*args): return _biogeme.vectorDouble_assign(*args)
    def resize(*args): return _biogeme.vectorDouble_resize(*args)
    def insert(*args): return _biogeme.vectorDouble_insert(*args)
    def reserve(*args): return _biogeme.vectorDouble_reserve(*args)
    def capacity(*args): return _biogeme.vectorDouble_capacity(*args)
    __swig_destroy__ = _biogeme.delete_vectorDouble
    __del__ = lambda self : None;
vectorDouble_swigregister = _biogeme.vectorDouble_swigregister
vectorDouble_swigregister(vectorDouble)

class vectorStr(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, vectorStr, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, vectorStr, name)
    __repr__ = _swig_repr
    def iterator(*args): return _biogeme.vectorStr_iterator(*args)
    def __iter__(self): return self.iterator()
    def __nonzero__(*args): return _biogeme.vectorStr___nonzero__(*args)
    def __len__(*args): return _biogeme.vectorStr___len__(*args)
    def pop(*args): return _biogeme.vectorStr_pop(*args)
    def __getslice__(*args): return _biogeme.vectorStr___getslice__(*args)
    def __setslice__(*args): return _biogeme.vectorStr___setslice__(*args)
    def __delslice__(*args): return _biogeme.vectorStr___delslice__(*args)
    def __delitem__(*args): return _biogeme.vectorStr___delitem__(*args)
    def __getitem__(*args): return _biogeme.vectorStr___getitem__(*args)
    def __setitem__(*args): return _biogeme.vectorStr___setitem__(*args)
    def append(*args): return _biogeme.vectorStr_append(*args)
    def empty(*args): return _biogeme.vectorStr_empty(*args)
    def size(*args): return _biogeme.vectorStr_size(*args)
    def clear(*args): return _biogeme.vectorStr_clear(*args)
    def swap(*args): return _biogeme.vectorStr_swap(*args)
    def get_allocator(*args): return _biogeme.vectorStr_get_allocator(*args)
    def begin(*args): return _biogeme.vectorStr_begin(*args)
    def end(*args): return _biogeme.vectorStr_end(*args)
    def rbegin(*args): return _biogeme.vectorStr_rbegin(*args)
    def rend(*args): return _biogeme.vectorStr_rend(*args)
    def pop_back(*args): return _biogeme.vectorStr_pop_back(*args)
    def erase(*args): return _biogeme.vectorStr_erase(*args)
    def __init__(self, *args): 
        this = _biogeme.new_vectorStr(*args)
        try: self.this.append(this)
        except: self.this = this
    def push_back(*args): return _biogeme.vectorStr_push_back(*args)
    def front(*args): return _biogeme.vectorStr_front(*args)
    def back(*args): return _biogeme.vectorStr_back(*args)
    def assign(*args): return _biogeme.vectorStr_assign(*args)
    def resize(*args): return _biogeme.vectorStr_resize(*args)
    def insert(*args): return _biogeme.vectorStr_insert(*args)
    def reserve(*args): return _biogeme.vectorStr_reserve(*args)
    def capacity(*args): return _biogeme.vectorStr_capacity(*args)
    __swig_destroy__ = _biogeme.delete_vectorStr
    __del__ = lambda self : None;
vectorStr_swigregister = _biogeme.vectorStr_swigregister
vectorStr_swigregister(vectorStr)

class patPythonResults(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, patPythonResults, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, patPythonResults, name)
    __repr__ = _swig_repr
    def getTimeStamp(*args): return _biogeme.patPythonResults_getTimeStamp(*args)
    def getVersion(*args): return _biogeme.patPythonResults_getVersion(*args)
    def getDescription(*args): return _biogeme.patPythonResults_getDescription(*args)
    def getModel(*args): return _biogeme.patPythonResults_getModel(*args)
    def getDrawsType(*args): return _biogeme.patPythonResults_getDrawsType(*args)
    __swig_setmethods__["numberOfDraws"] = _biogeme.patPythonResults_numberOfDraws_set
    __swig_getmethods__["numberOfDraws"] = _biogeme.patPythonResults_numberOfDraws_get
    if _newclass:numberOfDraws = property(_biogeme.patPythonResults_numberOfDraws_get, _biogeme.patPythonResults_numberOfDraws_set)
    __swig_setmethods__["numberOfParameters"] = _biogeme.patPythonResults_numberOfParameters_set
    __swig_getmethods__["numberOfParameters"] = _biogeme.patPythonResults_numberOfParameters_get
    if _newclass:numberOfParameters = property(_biogeme.patPythonResults_numberOfParameters_get, _biogeme.patPythonResults_numberOfParameters_set)
    __swig_setmethods__["numberOfObservations"] = _biogeme.patPythonResults_numberOfObservations_set
    __swig_getmethods__["numberOfObservations"] = _biogeme.patPythonResults_numberOfObservations_get
    if _newclass:numberOfObservations = property(_biogeme.patPythonResults_numberOfObservations_get, _biogeme.patPythonResults_numberOfObservations_set)
    __swig_setmethods__["numberOfIndividuals"] = _biogeme.patPythonResults_numberOfIndividuals_set
    __swig_getmethods__["numberOfIndividuals"] = _biogeme.patPythonResults_numberOfIndividuals_get
    if _newclass:numberOfIndividuals = property(_biogeme.patPythonResults_numberOfIndividuals_get, _biogeme.patPythonResults_numberOfIndividuals_set)
    __swig_setmethods__["nullLoglikelihood"] = _biogeme.patPythonResults_nullLoglikelihood_set
    __swig_getmethods__["nullLoglikelihood"] = _biogeme.patPythonResults_nullLoglikelihood_get
    if _newclass:nullLoglikelihood = property(_biogeme.patPythonResults_nullLoglikelihood_get, _biogeme.patPythonResults_nullLoglikelihood_set)
    __swig_setmethods__["initLoglikelihood"] = _biogeme.patPythonResults_initLoglikelihood_set
    __swig_getmethods__["initLoglikelihood"] = _biogeme.patPythonResults_initLoglikelihood_get
    if _newclass:initLoglikelihood = property(_biogeme.patPythonResults_initLoglikelihood_get, _biogeme.patPythonResults_initLoglikelihood_set)
    __swig_setmethods__["finalLoglikelihood"] = _biogeme.patPythonResults_finalLoglikelihood_set
    __swig_getmethods__["finalLoglikelihood"] = _biogeme.patPythonResults_finalLoglikelihood_get
    if _newclass:finalLoglikelihood = property(_biogeme.patPythonResults_finalLoglikelihood_get, _biogeme.patPythonResults_finalLoglikelihood_set)
    __swig_setmethods__["likelihoodRatioTest"] = _biogeme.patPythonResults_likelihoodRatioTest_set
    __swig_getmethods__["likelihoodRatioTest"] = _biogeme.patPythonResults_likelihoodRatioTest_get
    if _newclass:likelihoodRatioTest = property(_biogeme.patPythonResults_likelihoodRatioTest_get, _biogeme.patPythonResults_likelihoodRatioTest_set)
    __swig_setmethods__["rhoSquare"] = _biogeme.patPythonResults_rhoSquare_set
    __swig_getmethods__["rhoSquare"] = _biogeme.patPythonResults_rhoSquare_get
    if _newclass:rhoSquare = property(_biogeme.patPythonResults_rhoSquare_get, _biogeme.patPythonResults_rhoSquare_set)
    __swig_setmethods__["rhoBarSquare"] = _biogeme.patPythonResults_rhoBarSquare_set
    __swig_getmethods__["rhoBarSquare"] = _biogeme.patPythonResults_rhoBarSquare_get
    if _newclass:rhoBarSquare = property(_biogeme.patPythonResults_rhoBarSquare_get, _biogeme.patPythonResults_rhoBarSquare_set)
    __swig_setmethods__["finalGradientNorm"] = _biogeme.patPythonResults_finalGradientNorm_set
    __swig_getmethods__["finalGradientNorm"] = _biogeme.patPythonResults_finalGradientNorm_get
    if _newclass:finalGradientNorm = property(_biogeme.patPythonResults_finalGradientNorm_get, _biogeme.patPythonResults_finalGradientNorm_set)
    def getVarianceCovariance(*args): return _biogeme.patPythonResults_getVarianceCovariance(*args)
    __swig_setmethods__["totalNumberOfParameters"] = _biogeme.patPythonResults_totalNumberOfParameters_set
    __swig_getmethods__["totalNumberOfParameters"] = _biogeme.patPythonResults_totalNumberOfParameters_get
    if _newclass:totalNumberOfParameters = property(_biogeme.patPythonResults_totalNumberOfParameters_get, _biogeme.patPythonResults_totalNumberOfParameters_set)
    def getParamName(*args): return _biogeme.patPythonResults_getParamName(*args)
    def getEstimate(*args): return _biogeme.patPythonResults_getEstimate(*args)
    def getStdErr(*args): return _biogeme.patPythonResults_getStdErr(*args)
    def getTTest(*args): return _biogeme.patPythonResults_getTTest(*args)
    def getPValue(*args): return _biogeme.patPythonResults_getPValue(*args)
    def getStdErrRobust(*args): return _biogeme.patPythonResults_getStdErrRobust(*args)
    def getTTestRobust(*args): return _biogeme.patPythonResults_getTTestRobust(*args)
    def getPValueRobust(*args): return _biogeme.patPythonResults_getPValueRobust(*args)
    def getFixed(*args): return _biogeme.patPythonResults_getFixed(*args)
    def getDistributed(*args): return _biogeme.patPythonResults_getDistributed(*args)
    def __init__(self, *args): 
        this = _biogeme.new_patPythonResults(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _biogeme.delete_patPythonResults
    __del__ = lambda self : None;
patPythonResults_swigregister = _biogeme.patPythonResults_swigregister
patPythonResults_swigregister(patPythonResults)

class patBiogemeScripting(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, patBiogemeScripting, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, patBiogemeScripting, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _biogeme.new_patBiogemeScripting(*args)
        try: self.this.append(this)
        except: self.this = this
    def estimate(*args): return _biogeme.patBiogemeScripting_estimate(*args)
    def simulate(*args): return _biogeme.patBiogemeScripting_simulate(*args)
    __swig_destroy__ = _biogeme.delete_patBiogemeScripting
    __del__ = lambda self : None;
patBiogemeScripting_swigregister = _biogeme.patBiogemeScripting_swigregister
patBiogemeScripting_swigregister(patBiogemeScripting)



