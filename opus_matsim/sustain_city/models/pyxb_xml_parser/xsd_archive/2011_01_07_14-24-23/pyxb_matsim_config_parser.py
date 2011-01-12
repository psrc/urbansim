# Opus/UrbanSim urban simulation software
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

# ./pyxb_matsim_config_parser.py
# PyXB bindings for NamespaceModule
# NSM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2011-01-06 15:52:38.427125 by PyXB version 1.1.1
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:9aca414f-19a4-11e0-9f73-001b63930ac1')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

Namespace = pyxb.namespace.CreateAbsentNamespace()
Namespace.configureCategories(['typeBinding', 'elementBinding'])
ModuleRecord = Namespace.lookupModuleRecordByUID(_GenerationUID, create_if_missing=True)
ModuleRecord._setModule(sys.modules[__name__])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a Python instance."""
    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement)
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=Namespace.fallbackNamespace(), location_base=location_base)
    handler = saxer.getContentHandler()
    saxer.parse(StringIO.StringIO(xml_text))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, _fallback_namespace=default_namespace)


# Complex type networkType with content type ELEMENT_ONLY
class networkType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'networkType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element inputFile uses Python identifier inputFile
    __inputFile = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'inputFile'), 'inputFile', '__AbsentNamespace0_networkType_inputFile', False)

    
    inputFile = property(__inputFile.value, __inputFile.set, None, None)


    _ElementMap = {
        __inputFile.name() : __inputFile
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'networkType', networkType)


# Complex type matsim_configType with content type ELEMENT_ONLY
class matsim_configType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'matsim_configType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element matsim4urbansim uses Python identifier matsim4urbansim
    __matsim4urbansim = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'matsim4urbansim'), 'matsim4urbansim', '__AbsentNamespace0_matsim_configType_matsim4urbansim', False)

    
    matsim4urbansim = property(__matsim4urbansim.value, __matsim4urbansim.set, None, None)

    
    # Element config uses Python identifier config
    __config = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'config'), 'config', '__AbsentNamespace0_matsim_configType_config', False)

    
    config = property(__config.value, __config.set, None, None)


    _ElementMap = {
        __matsim4urbansim.name() : __matsim4urbansim,
        __config.name() : __config
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'matsim_configType', matsim_configType)


# Complex type controlerType with content type ELEMENT_ONLY
class controlerType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'controlerType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element lastIteration uses Python identifier lastIteration
    __lastIteration = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'lastIteration'), 'lastIteration', '__AbsentNamespace0_controlerType_lastIteration', False)

    
    lastIteration = property(__lastIteration.value, __lastIteration.set, None, None)

    
    # Element firstIteration uses Python identifier firstIteration
    __firstIteration = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'firstIteration'), 'firstIteration', '__AbsentNamespace0_controlerType_firstIteration', False)

    
    firstIteration = property(__firstIteration.value, __firstIteration.set, None, None)


    _ElementMap = {
        __lastIteration.name() : __lastIteration,
        __firstIteration.name() : __firstIteration
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'controlerType', controlerType)


# Complex type planCalcScoreType with content type ELEMENT_ONLY
class planCalcScoreType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'planCalcScoreType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element activityType_1 uses Python identifier activityType_1
    __activityType_1 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'activityType_1'), 'activityType_1', '__AbsentNamespace0_planCalcScoreType_activityType_1', False)

    
    activityType_1 = property(__activityType_1.value, __activityType_1.set, None, None)

    
    # Element activityType_0 uses Python identifier activityType_0
    __activityType_0 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'activityType_0'), 'activityType_0', '__AbsentNamespace0_planCalcScoreType_activityType_0', False)

    
    activityType_0 = property(__activityType_0.value, __activityType_0.set, None, None)


    _ElementMap = {
        __activityType_1.name() : __activityType_1,
        __activityType_0.name() : __activityType_0
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'planCalcScoreType', planCalcScoreType)


# Complex type configType with content type ELEMENT_ONLY
class configType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'configType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element planCalcScore uses Python identifier planCalcScore
    __planCalcScore = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'planCalcScore'), 'planCalcScore', '__AbsentNamespace0_configType_planCalcScore', False)

    
    planCalcScore = property(__planCalcScore.value, __planCalcScore.set, None, None)

    
    # Element network uses Python identifier network
    __network = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'network'), 'network', '__AbsentNamespace0_configType_network', False)

    
    network = property(__network.value, __network.set, None, None)

    
    # Element controler uses Python identifier controler
    __controler = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'controler'), 'controler', '__AbsentNamespace0_configType_controler', False)

    
    controler = property(__controler.value, __controler.set, None, None)


    _ElementMap = {
        __planCalcScore.name() : __planCalcScore,
        __network.name() : __network,
        __controler.name() : __controler
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'configType', configType)


# Complex type matsim4urbansimType with content type ELEMENT_ONLY
class matsim4urbansimType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'matsim4urbansimType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element urbansimParameter uses Python identifier urbansimParameter
    __urbansimParameter = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'urbansimParameter'), 'urbansimParameter', '__AbsentNamespace0_matsim4urbansimType_urbansimParameter', False)

    
    urbansimParameter = property(__urbansimParameter.value, __urbansimParameter.set, None, None)


    _ElementMap = {
        __urbansimParameter.name() : __urbansimParameter
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'matsim4urbansimType', matsim4urbansimType)


# Complex type urbansimParameterType with content type ELEMENT_ONLY
class urbansimParameterType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'urbansimParameterType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element opusHOME uses Python identifier opusHOME
    __opusHOME = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'opusHOME'), 'opusHOME', '__AbsentNamespace0_urbansimParameterType_opusHOME', False)

    
    opusHOME = property(__opusHOME.value, __opusHOME.set, None, None)

    
    # Element samplingRate uses Python identifier samplingRate
    __samplingRate = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'samplingRate'), 'samplingRate', '__AbsentNamespace0_urbansimParameterType_samplingRate', False)

    
    samplingRate = property(__samplingRate.value, __samplingRate.set, None, None)

    
    # Element tempDirectory uses Python identifier tempDirectory
    __tempDirectory = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'tempDirectory'), 'tempDirectory', '__AbsentNamespace0_urbansimParameterType_tempDirectory', False)

    
    tempDirectory = property(__tempDirectory.value, __tempDirectory.set, None, None)

    
    # Element year uses Python identifier year
    __year = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'year'), 'year', '__AbsentNamespace0_urbansimParameterType_year', False)

    
    year = property(__year.value, __year.set, None, None)

    
    # Element isTestRun uses Python identifier isTestRun
    __isTestRun = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'isTestRun'), 'isTestRun', '__AbsentNamespace0_urbansimParameterType_isTestRun', False)

    
    isTestRun = property(__isTestRun.value, __isTestRun.set, None, None)


    _ElementMap = {
        __opusHOME.name() : __opusHOME,
        __samplingRate.name() : __samplingRate,
        __tempDirectory.name() : __tempDirectory,
        __year.name() : __year,
        __isTestRun.name() : __isTestRun
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'urbansimParameterType', urbansimParameterType)


matsim_config = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'matsim_config'), matsim_configType)
Namespace.addCategoryObject('elementBinding', matsim_config.name().localName(), matsim_config)



networkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'inputFile'), pyxb.binding.datatypes.token, scope=networkType))
networkType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=networkType._UseForTag(pyxb.namespace.ExpandedName(None, u'inputFile'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})



matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'matsim4urbansim'), matsim4urbansimType, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'config'), configType, scope=matsim_configType))
matsim_configType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, u'config'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, u'matsim4urbansim'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
    ])
})



controlerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'lastIteration'), pyxb.binding.datatypes.nonNegativeInteger, scope=controlerType))

controlerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'firstIteration'), pyxb.binding.datatypes.nonNegativeInteger, scope=controlerType))
controlerType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=controlerType._UseForTag(pyxb.namespace.ExpandedName(None, u'firstIteration'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=controlerType._UseForTag(pyxb.namespace.ExpandedName(None, u'lastIteration'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
    ])
})



planCalcScoreType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'activityType_1'), pyxb.binding.datatypes.token, scope=planCalcScoreType))

planCalcScoreType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'activityType_0'), pyxb.binding.datatypes.token, scope=planCalcScoreType))
planCalcScoreType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=planCalcScoreType._UseForTag(pyxb.namespace.ExpandedName(None, u'activityType_0'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=planCalcScoreType._UseForTag(pyxb.namespace.ExpandedName(None, u'activityType_1'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
    ])
})



configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'planCalcScore'), planCalcScoreType, scope=configType))

configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'network'), networkType, scope=configType))

configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'controler'), controlerType, scope=configType))
configType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=configType._UseForTag(pyxb.namespace.ExpandedName(None, u'network'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=configType._UseForTag(pyxb.namespace.ExpandedName(None, u'controler'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=configType._UseForTag(pyxb.namespace.ExpandedName(None, u'planCalcScore'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
    ])
})



matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'urbansimParameter'), urbansimParameterType, scope=matsim4urbansimType))
matsim4urbansimType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, u'urbansimParameter'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})



urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'opusHOME'), pyxb.binding.datatypes.token, scope=urbansimParameterType))

urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'samplingRate'), pyxb.binding.datatypes.double, scope=urbansimParameterType))

urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'tempDirectory'), pyxb.binding.datatypes.token, scope=urbansimParameterType))

urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'year'), pyxb.binding.datatypes.nonNegativeInteger, scope=urbansimParameterType))

urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'isTestRun'), pyxb.binding.datatypes.boolean, scope=urbansimParameterType))
urbansimParameterType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'samplingRate'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'year'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'tempDirectory'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'isTestRun'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'opusHOME'))),
    ])
    , 6 : pyxb.binding.content.ContentModelState(state=6, is_final=True, transitions=[
    ])
})
