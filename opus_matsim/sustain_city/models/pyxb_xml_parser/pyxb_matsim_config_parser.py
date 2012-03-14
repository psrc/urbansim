# Opus/UrbanSim urban simulation software
# Copyright (C) 2010-2012 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

# ./pyxb_matsim_config_parser.py
# PyXB bindings for NM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2012-03-14 17:04:43.510150 by PyXB version 1.1.3
# Namespace AbsentNamespace0

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:6964bc45-6def-11e1-a4c6-3c07544cd942')

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


# Complex type urbansimParameterType with content type ELEMENT_ONLY
class urbansimParameterType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'urbansimParameterType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element samplingRate uses Python identifier samplingRate
    __samplingRate = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'samplingRate'), 'samplingRate', '__AbsentNamespace0_urbansimParameterType_samplingRate', False)

    
    samplingRate = property(__samplingRate.value, __samplingRate.set, None, None)

    
    # Element matsim4opusConfig uses Python identifier matsim4opusConfig
    __matsim4opusConfig = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'matsim4opusConfig'), 'matsim4opusConfig', '__AbsentNamespace0_urbansimParameterType_matsim4opusConfig', False)

    
    matsim4opusConfig = property(__matsim4opusConfig.value, __matsim4opusConfig.set, None, None)

    
    # Element year uses Python identifier year
    __year = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'year'), 'year', '__AbsentNamespace0_urbansimParameterType_year', False)

    
    year = property(__year.value, __year.set, None, None)

    
    # Element opusHome uses Python identifier opusHome
    __opusHome = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'opusHome'), 'opusHome', '__AbsentNamespace0_urbansimParameterType_opusHome', False)

    
    opusHome = property(__opusHome.value, __opusHome.set, None, None)

    
    # Element opusDataPath uses Python identifier opusDataPath
    __opusDataPath = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'opusDataPath'), 'opusDataPath', '__AbsentNamespace0_urbansimParameterType_opusDataPath', False)

    
    opusDataPath = property(__opusDataPath.value, __opusDataPath.set, None, None)

    
    # Element isTestRun uses Python identifier isTestRun
    __isTestRun = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'isTestRun'), 'isTestRun', '__AbsentNamespace0_urbansimParameterType_isTestRun', False)

    
    isTestRun = property(__isTestRun.value, __isTestRun.set, None, None)

    
    # Element matsim4opus uses Python identifier matsim4opus
    __matsim4opus = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'matsim4opus'), 'matsim4opus', '__AbsentNamespace0_urbansimParameterType_matsim4opus', False)

    
    matsim4opus = property(__matsim4opus.value, __matsim4opus.set, None, None)

    
    # Element testParameter uses Python identifier testParameter
    __testParameter = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'testParameter'), 'testParameter', '__AbsentNamespace0_urbansimParameterType_testParameter', False)

    
    testParameter = property(__testParameter.value, __testParameter.set, None, None)

    
    # Element matsim4opusOutput uses Python identifier matsim4opusOutput
    __matsim4opusOutput = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'matsim4opusOutput'), 'matsim4opusOutput', '__AbsentNamespace0_urbansimParameterType_matsim4opusOutput', False)

    
    matsim4opusOutput = property(__matsim4opusOutput.value, __matsim4opusOutput.set, None, None)

    
    # Element backupRunData uses Python identifier backupRunData
    __backupRunData = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'backupRunData'), 'backupRunData', '__AbsentNamespace0_urbansimParameterType_backupRunData', False)

    
    backupRunData = property(__backupRunData.value, __backupRunData.set, None, None)

    
    # Element matsim4opusTemp uses Python identifier matsim4opusTemp
    __matsim4opusTemp = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'matsim4opusTemp'), 'matsim4opusTemp', '__AbsentNamespace0_urbansimParameterType_matsim4opusTemp', False)

    
    matsim4opusTemp = property(__matsim4opusTemp.value, __matsim4opusTemp.set, None, None)


    _ElementMap = {
        __samplingRate.name() : __samplingRate,
        __matsim4opusConfig.name() : __matsim4opusConfig,
        __year.name() : __year,
        __opusHome.name() : __opusHome,
        __opusDataPath.name() : __opusDataPath,
        __isTestRun.name() : __isTestRun,
        __matsim4opus.name() : __matsim4opus,
        __testParameter.name() : __testParameter,
        __matsim4opusOutput.name() : __matsim4opusOutput,
        __backupRunData.name() : __backupRunData,
        __matsim4opusTemp.name() : __matsim4opusTemp
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'urbansimParameterType', urbansimParameterType)


# Complex type matsim4urbansimType with content type ELEMENT_ONLY
class matsim4urbansimType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'matsim4urbansimType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element accessibilityParameter uses Python identifier accessibilityParameter
    __accessibilityParameter = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'accessibilityParameter'), 'accessibilityParameter', '__AbsentNamespace0_matsim4urbansimType_accessibilityParameter', False)

    
    accessibilityParameter = property(__accessibilityParameter.value, __accessibilityParameter.set, None, None)

    
    # Element urbansimParameter uses Python identifier urbansimParameter
    __urbansimParameter = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'urbansimParameter'), 'urbansimParameter', '__AbsentNamespace0_matsim4urbansimType_urbansimParameter', False)

    
    urbansimParameter = property(__urbansimParameter.value, __urbansimParameter.set, None, None)

    
    # Element matsim4urbansimContoler uses Python identifier matsim4urbansimContoler
    __matsim4urbansimContoler = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'matsim4urbansimContoler'), 'matsim4urbansimContoler', '__AbsentNamespace0_matsim4urbansimType_matsim4urbansimContoler', False)

    
    matsim4urbansimContoler = property(__matsim4urbansimContoler.value, __matsim4urbansimContoler.set, None, None)


    _ElementMap = {
        __accessibilityParameter.name() : __accessibilityParameter,
        __urbansimParameter.name() : __urbansimParameter,
        __matsim4urbansimContoler.name() : __matsim4urbansimContoler
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'matsim4urbansimType', matsim4urbansimType)


# Complex type accessibilityParameterType with content type ELEMENT_ONLY
class accessibilityParameterType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'accessibilityParameterType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element useLogitScaleParameterFromMATSim uses Python identifier useLogitScaleParameterFromMATSim
    __useLogitScaleParameterFromMATSim = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'useLogitScaleParameterFromMATSim'), 'useLogitScaleParameterFromMATSim', '__AbsentNamespace0_accessibilityParameterType_useLogitScaleParameterFromMATSim', False)

    
    useLogitScaleParameterFromMATSim = property(__useLogitScaleParameterFromMATSim.value, __useLogitScaleParameterFromMATSim.set, None, None)

    
    # Element useWalkParameterFromMATSim uses Python identifier useWalkParameterFromMATSim
    __useWalkParameterFromMATSim = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'useWalkParameterFromMATSim'), 'useWalkParameterFromMATSim', '__AbsentNamespace0_accessibilityParameterType_useWalkParameterFromMATSim', False)

    
    useWalkParameterFromMATSim = property(__useWalkParameterFromMATSim.value, __useWalkParameterFromMATSim.set, None, None)

    
    # Element useRawSumsWithoutLn uses Python identifier useRawSumsWithoutLn
    __useRawSumsWithoutLn = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'useRawSumsWithoutLn'), 'useRawSumsWithoutLn', '__AbsentNamespace0_accessibilityParameterType_useRawSumsWithoutLn', False)

    
    useRawSumsWithoutLn = property(__useRawSumsWithoutLn.value, __useRawSumsWithoutLn.set, None, None)

    
    # Element logitScaleParameter uses Python identifier logitScaleParameter
    __logitScaleParameter = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'logitScaleParameter'), 'logitScaleParameter', '__AbsentNamespace0_accessibilityParameterType_logitScaleParameter', False)

    
    logitScaleParameter = property(__logitScaleParameter.value, __logitScaleParameter.set, None, None)

    
    # Element betaCarTravelTimePower2 uses Python identifier betaCarTravelTimePower2
    __betaCarTravelTimePower2 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'betaCarTravelTimePower2'), 'betaCarTravelTimePower2', '__AbsentNamespace0_accessibilityParameterType_betaCarTravelTimePower2', False)

    
    betaCarTravelTimePower2 = property(__betaCarTravelTimePower2.value, __betaCarTravelTimePower2.set, None, None)

    
    # Element betaCarTravelTime uses Python identifier betaCarTravelTime
    __betaCarTravelTime = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'betaCarTravelTime'), 'betaCarTravelTime', '__AbsentNamespace0_accessibilityParameterType_betaCarTravelTime', False)

    
    betaCarTravelTime = property(__betaCarTravelTime.value, __betaCarTravelTime.set, None, None)

    
    # Element betaWalkLnTravelDistance uses Python identifier betaWalkLnTravelDistance
    __betaWalkLnTravelDistance = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'betaWalkLnTravelDistance'), 'betaWalkLnTravelDistance', '__AbsentNamespace0_accessibilityParameterType_betaWalkLnTravelDistance', False)

    
    betaWalkLnTravelDistance = property(__betaWalkLnTravelDistance.value, __betaWalkLnTravelDistance.set, None, None)

    
    # Element betaCarLnTravelTime uses Python identifier betaCarLnTravelTime
    __betaCarLnTravelTime = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'betaCarLnTravelTime'), 'betaCarLnTravelTime', '__AbsentNamespace0_accessibilityParameterType_betaCarLnTravelTime', False)

    
    betaCarLnTravelTime = property(__betaCarLnTravelTime.value, __betaCarLnTravelTime.set, None, None)

    
    # Element betaCarTravelDistance uses Python identifier betaCarTravelDistance
    __betaCarTravelDistance = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'betaCarTravelDistance'), 'betaCarTravelDistance', '__AbsentNamespace0_accessibilityParameterType_betaCarTravelDistance', False)

    
    betaCarTravelDistance = property(__betaCarTravelDistance.value, __betaCarTravelDistance.set, None, None)

    
    # Element betaCarTravelDistancePower2 uses Python identifier betaCarTravelDistancePower2
    __betaCarTravelDistancePower2 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'betaCarTravelDistancePower2'), 'betaCarTravelDistancePower2', '__AbsentNamespace0_accessibilityParameterType_betaCarTravelDistancePower2', False)

    
    betaCarTravelDistancePower2 = property(__betaCarTravelDistancePower2.value, __betaCarTravelDistancePower2.set, None, None)

    
    # Element betaCarLnTravelDistance uses Python identifier betaCarLnTravelDistance
    __betaCarLnTravelDistance = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'betaCarLnTravelDistance'), 'betaCarLnTravelDistance', '__AbsentNamespace0_accessibilityParameterType_betaCarLnTravelDistance', False)

    
    betaCarLnTravelDistance = property(__betaCarLnTravelDistance.value, __betaCarLnTravelDistance.set, None, None)

    
    # Element betaCarTravelCost uses Python identifier betaCarTravelCost
    __betaCarTravelCost = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'betaCarTravelCost'), 'betaCarTravelCost', '__AbsentNamespace0_accessibilityParameterType_betaCarTravelCost', False)

    
    betaCarTravelCost = property(__betaCarTravelCost.value, __betaCarTravelCost.set, None, None)

    
    # Element betaCarTravelCostPower2 uses Python identifier betaCarTravelCostPower2
    __betaCarTravelCostPower2 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'betaCarTravelCostPower2'), 'betaCarTravelCostPower2', '__AbsentNamespace0_accessibilityParameterType_betaCarTravelCostPower2', False)

    
    betaCarTravelCostPower2 = property(__betaCarTravelCostPower2.value, __betaCarTravelCostPower2.set, None, None)

    
    # Element betaCarLnTravelCost uses Python identifier betaCarLnTravelCost
    __betaCarLnTravelCost = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'betaCarLnTravelCost'), 'betaCarLnTravelCost', '__AbsentNamespace0_accessibilityParameterType_betaCarLnTravelCost', False)

    
    betaCarLnTravelCost = property(__betaCarLnTravelCost.value, __betaCarLnTravelCost.set, None, None)

    
    # Element betaWalkTravelTime uses Python identifier betaWalkTravelTime
    __betaWalkTravelTime = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'betaWalkTravelTime'), 'betaWalkTravelTime', '__AbsentNamespace0_accessibilityParameterType_betaWalkTravelTime', False)

    
    betaWalkTravelTime = property(__betaWalkTravelTime.value, __betaWalkTravelTime.set, None, None)

    
    # Element betaWalkLnTravelTime uses Python identifier betaWalkLnTravelTime
    __betaWalkLnTravelTime = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'betaWalkLnTravelTime'), 'betaWalkLnTravelTime', '__AbsentNamespace0_accessibilityParameterType_betaWalkLnTravelTime', False)

    
    betaWalkLnTravelTime = property(__betaWalkLnTravelTime.value, __betaWalkLnTravelTime.set, None, None)

    
    # Element betaWalkTravelDistance uses Python identifier betaWalkTravelDistance
    __betaWalkTravelDistance = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'betaWalkTravelDistance'), 'betaWalkTravelDistance', '__AbsentNamespace0_accessibilityParameterType_betaWalkTravelDistance', False)

    
    betaWalkTravelDistance = property(__betaWalkTravelDistance.value, __betaWalkTravelDistance.set, None, None)

    
    # Element betaWalkTravelDistancePower2 uses Python identifier betaWalkTravelDistancePower2
    __betaWalkTravelDistancePower2 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'betaWalkTravelDistancePower2'), 'betaWalkTravelDistancePower2', '__AbsentNamespace0_accessibilityParameterType_betaWalkTravelDistancePower2', False)

    
    betaWalkTravelDistancePower2 = property(__betaWalkTravelDistancePower2.value, __betaWalkTravelDistancePower2.set, None, None)

    
    # Element betaWalkTravelTimePower2 uses Python identifier betaWalkTravelTimePower2
    __betaWalkTravelTimePower2 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'betaWalkTravelTimePower2'), 'betaWalkTravelTimePower2', '__AbsentNamespace0_accessibilityParameterType_betaWalkTravelTimePower2', False)

    
    betaWalkTravelTimePower2 = property(__betaWalkTravelTimePower2.value, __betaWalkTravelTimePower2.set, None, None)

    
    # Element betaWalkTravelCost uses Python identifier betaWalkTravelCost
    __betaWalkTravelCost = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'betaWalkTravelCost'), 'betaWalkTravelCost', '__AbsentNamespace0_accessibilityParameterType_betaWalkTravelCost', False)

    
    betaWalkTravelCost = property(__betaWalkTravelCost.value, __betaWalkTravelCost.set, None, None)

    
    # Element betaWalkTravelCostPower2 uses Python identifier betaWalkTravelCostPower2
    __betaWalkTravelCostPower2 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'betaWalkTravelCostPower2'), 'betaWalkTravelCostPower2', '__AbsentNamespace0_accessibilityParameterType_betaWalkTravelCostPower2', False)

    
    betaWalkTravelCostPower2 = property(__betaWalkTravelCostPower2.value, __betaWalkTravelCostPower2.set, None, None)

    
    # Element betaWalkLnTravelCost uses Python identifier betaWalkLnTravelCost
    __betaWalkLnTravelCost = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'betaWalkLnTravelCost'), 'betaWalkLnTravelCost', '__AbsentNamespace0_accessibilityParameterType_betaWalkLnTravelCost', False)

    
    betaWalkLnTravelCost = property(__betaWalkLnTravelCost.value, __betaWalkLnTravelCost.set, None, None)

    
    # Element useCarParameterFromMATSim uses Python identifier useCarParameterFromMATSim
    __useCarParameterFromMATSim = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'useCarParameterFromMATSim'), 'useCarParameterFromMATSim', '__AbsentNamespace0_accessibilityParameterType_useCarParameterFromMATSim', False)

    
    useCarParameterFromMATSim = property(__useCarParameterFromMATSim.value, __useCarParameterFromMATSim.set, None, None)


    _ElementMap = {
        __useLogitScaleParameterFromMATSim.name() : __useLogitScaleParameterFromMATSim,
        __useWalkParameterFromMATSim.name() : __useWalkParameterFromMATSim,
        __useRawSumsWithoutLn.name() : __useRawSumsWithoutLn,
        __logitScaleParameter.name() : __logitScaleParameter,
        __betaCarTravelTimePower2.name() : __betaCarTravelTimePower2,
        __betaCarTravelTime.name() : __betaCarTravelTime,
        __betaWalkLnTravelDistance.name() : __betaWalkLnTravelDistance,
        __betaCarLnTravelTime.name() : __betaCarLnTravelTime,
        __betaCarTravelDistance.name() : __betaCarTravelDistance,
        __betaCarTravelDistancePower2.name() : __betaCarTravelDistancePower2,
        __betaCarLnTravelDistance.name() : __betaCarLnTravelDistance,
        __betaCarTravelCost.name() : __betaCarTravelCost,
        __betaCarTravelCostPower2.name() : __betaCarTravelCostPower2,
        __betaCarLnTravelCost.name() : __betaCarLnTravelCost,
        __betaWalkTravelTime.name() : __betaWalkTravelTime,
        __betaWalkLnTravelTime.name() : __betaWalkLnTravelTime,
        __betaWalkTravelDistance.name() : __betaWalkTravelDistance,
        __betaWalkTravelDistancePower2.name() : __betaWalkTravelDistancePower2,
        __betaWalkTravelTimePower2.name() : __betaWalkTravelTimePower2,
        __betaWalkTravelCost.name() : __betaWalkTravelCost,
        __betaWalkTravelCostPower2.name() : __betaWalkTravelCostPower2,
        __betaWalkLnTravelCost.name() : __betaWalkLnTravelCost,
        __useCarParameterFromMATSim.name() : __useCarParameterFromMATSim
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'accessibilityParameterType', accessibilityParameterType)


# Complex type strategyType with content type ELEMENT_ONLY
class strategyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'strategyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element reRouteDijkstraProbability uses Python identifier reRouteDijkstraProbability
    __reRouteDijkstraProbability = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'reRouteDijkstraProbability'), 'reRouteDijkstraProbability', '__AbsentNamespace0_strategyType_reRouteDijkstraProbability', False)

    
    reRouteDijkstraProbability = property(__reRouteDijkstraProbability.value, __reRouteDijkstraProbability.set, None, None)

    
    # Element maxAgentPlanMemorySize uses Python identifier maxAgentPlanMemorySize
    __maxAgentPlanMemorySize = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'maxAgentPlanMemorySize'), 'maxAgentPlanMemorySize', '__AbsentNamespace0_strategyType_maxAgentPlanMemorySize', False)

    
    maxAgentPlanMemorySize = property(__maxAgentPlanMemorySize.value, __maxAgentPlanMemorySize.set, None, None)

    
    # Element changeExpBetaProbability uses Python identifier changeExpBetaProbability
    __changeExpBetaProbability = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'changeExpBetaProbability'), 'changeExpBetaProbability', '__AbsentNamespace0_strategyType_changeExpBetaProbability', False)

    
    changeExpBetaProbability = property(__changeExpBetaProbability.value, __changeExpBetaProbability.set, None, None)

    
    # Element timeAllocationMutatorProbability uses Python identifier timeAllocationMutatorProbability
    __timeAllocationMutatorProbability = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'timeAllocationMutatorProbability'), 'timeAllocationMutatorProbability', '__AbsentNamespace0_strategyType_timeAllocationMutatorProbability', False)

    
    timeAllocationMutatorProbability = property(__timeAllocationMutatorProbability.value, __timeAllocationMutatorProbability.set, None, None)


    _ElementMap = {
        __reRouteDijkstraProbability.name() : __reRouteDijkstraProbability,
        __maxAgentPlanMemorySize.name() : __maxAgentPlanMemorySize,
        __changeExpBetaProbability.name() : __changeExpBetaProbability,
        __timeAllocationMutatorProbability.name() : __timeAllocationMutatorProbability
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'strategyType', strategyType)


# Complex type fileType with content type ELEMENT_ONLY
class fileType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'fileType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element inputFile uses Python identifier inputFile
    __inputFile = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'inputFile'), 'inputFile', '__AbsentNamespace0_fileType_inputFile', False)

    
    inputFile = property(__inputFile.value, __inputFile.set, None, None)


    _ElementMap = {
        __inputFile.name() : __inputFile
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'fileType', fileType)


# Complex type inputPlansFileType with content type ELEMENT_ONLY
class inputPlansFileType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'inputPlansFileType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element inputFile uses Python identifier inputFile
    __inputFile = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'inputFile'), 'inputFile', '__AbsentNamespace0_inputPlansFileType_inputFile', False)

    
    inputFile = property(__inputFile.value, __inputFile.set, None, None)


    _ElementMap = {
        __inputFile.name() : __inputFile
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'inputPlansFileType', inputPlansFileType)


# Complex type planCalcScoreType with content type ELEMENT_ONLY
class planCalcScoreType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'planCalcScoreType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element activityType_0 uses Python identifier activityType_0
    __activityType_0 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'activityType_0'), 'activityType_0', '__AbsentNamespace0_planCalcScoreType_activityType_0', False)

    
    activityType_0 = property(__activityType_0.value, __activityType_0.set, None, None)

    
    # Element workActivityLatestStartTime uses Python identifier workActivityLatestStartTime
    __workActivityLatestStartTime = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'workActivityLatestStartTime'), 'workActivityLatestStartTime', '__AbsentNamespace0_planCalcScoreType_workActivityLatestStartTime', False)

    
    workActivityLatestStartTime = property(__workActivityLatestStartTime.value, __workActivityLatestStartTime.set, None, None)

    
    # Element activityType_1 uses Python identifier activityType_1
    __activityType_1 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'activityType_1'), 'activityType_1', '__AbsentNamespace0_planCalcScoreType_activityType_1', False)

    
    activityType_1 = property(__activityType_1.value, __activityType_1.set, None, None)

    
    # Element homeActivityTypicalDuration uses Python identifier homeActivityTypicalDuration
    __homeActivityTypicalDuration = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'homeActivityTypicalDuration'), 'homeActivityTypicalDuration', '__AbsentNamespace0_planCalcScoreType_homeActivityTypicalDuration', False)

    
    homeActivityTypicalDuration = property(__homeActivityTypicalDuration.value, __homeActivityTypicalDuration.set, None, None)

    
    # Element workActivityTypicalDuration uses Python identifier workActivityTypicalDuration
    __workActivityTypicalDuration = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'workActivityTypicalDuration'), 'workActivityTypicalDuration', '__AbsentNamespace0_planCalcScoreType_workActivityTypicalDuration', False)

    
    workActivityTypicalDuration = property(__workActivityTypicalDuration.value, __workActivityTypicalDuration.set, None, None)

    
    # Element workActivityOpeningTime uses Python identifier workActivityOpeningTime
    __workActivityOpeningTime = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'workActivityOpeningTime'), 'workActivityOpeningTime', '__AbsentNamespace0_planCalcScoreType_workActivityOpeningTime', False)

    
    workActivityOpeningTime = property(__workActivityOpeningTime.value, __workActivityOpeningTime.set, None, None)


    _ElementMap = {
        __activityType_0.name() : __activityType_0,
        __workActivityLatestStartTime.name() : __workActivityLatestStartTime,
        __activityType_1.name() : __activityType_1,
        __homeActivityTypicalDuration.name() : __homeActivityTypicalDuration,
        __workActivityTypicalDuration.name() : __workActivityTypicalDuration,
        __workActivityOpeningTime.name() : __workActivityOpeningTime
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'planCalcScoreType', planCalcScoreType)


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


# Complex type matsim4urbansimContolerType with content type ELEMENT_ONLY
class matsim4urbansimContolerType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'matsim4urbansimContolerType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element cellBasedAccessibility uses Python identifier cellBasedAccessibility
    __cellBasedAccessibility = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'cellBasedAccessibility'), 'cellBasedAccessibility', '__AbsentNamespace0_matsim4urbansimContolerType_cellBasedAccessibility', False)

    
    cellBasedAccessibility = property(__cellBasedAccessibility.value, __cellBasedAccessibility.set, None, None)

    
    # Element shapeFileCellBasedAccessibility uses Python identifier shapeFileCellBasedAccessibility
    __shapeFileCellBasedAccessibility = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'shapeFileCellBasedAccessibility'), 'shapeFileCellBasedAccessibility', '__AbsentNamespace0_matsim4urbansimContolerType_shapeFileCellBasedAccessibility', False)

    
    shapeFileCellBasedAccessibility = property(__shapeFileCellBasedAccessibility.value, __shapeFileCellBasedAccessibility.set, None, None)

    
    # Element boundingBoxTop uses Python identifier boundingBoxTop
    __boundingBoxTop = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'boundingBoxTop'), 'boundingBoxTop', '__AbsentNamespace0_matsim4urbansimContolerType_boundingBoxTop', False)

    
    boundingBoxTop = property(__boundingBoxTop.value, __boundingBoxTop.set, None, None)

    
    # Element cellSizeCellBasedAccessibility uses Python identifier cellSizeCellBasedAccessibility
    __cellSizeCellBasedAccessibility = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'cellSizeCellBasedAccessibility'), 'cellSizeCellBasedAccessibility', '__AbsentNamespace0_matsim4urbansimContolerType_cellSizeCellBasedAccessibility', False)

    
    cellSizeCellBasedAccessibility = property(__cellSizeCellBasedAccessibility.value, __cellSizeCellBasedAccessibility.set, None, None)

    
    # Element boundingBoxLeft uses Python identifier boundingBoxLeft
    __boundingBoxLeft = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'boundingBoxLeft'), 'boundingBoxLeft', '__AbsentNamespace0_matsim4urbansimContolerType_boundingBoxLeft', False)

    
    boundingBoxLeft = property(__boundingBoxLeft.value, __boundingBoxLeft.set, None, None)

    
    # Element zone2zoneImpedance uses Python identifier zone2zoneImpedance
    __zone2zoneImpedance = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'zone2zoneImpedance'), 'zone2zoneImpedance', '__AbsentNamespace0_matsim4urbansimContolerType_zone2zoneImpedance', False)

    
    zone2zoneImpedance = property(__zone2zoneImpedance.value, __zone2zoneImpedance.set, None, None)

    
    # Element boundingBoxRight uses Python identifier boundingBoxRight
    __boundingBoxRight = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'boundingBoxRight'), 'boundingBoxRight', '__AbsentNamespace0_matsim4urbansimContolerType_boundingBoxRight', False)

    
    boundingBoxRight = property(__boundingBoxRight.value, __boundingBoxRight.set, None, None)

    
    # Element agentPerformance uses Python identifier agentPerformance
    __agentPerformance = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'agentPerformance'), 'agentPerformance', '__AbsentNamespace0_matsim4urbansimContolerType_agentPerformance', False)

    
    agentPerformance = property(__agentPerformance.value, __agentPerformance.set, None, None)

    
    # Element boundingBoxBottom uses Python identifier boundingBoxBottom
    __boundingBoxBottom = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'boundingBoxBottom'), 'boundingBoxBottom', '__AbsentNamespace0_matsim4urbansimContolerType_boundingBoxBottom', False)

    
    boundingBoxBottom = property(__boundingBoxBottom.value, __boundingBoxBottom.set, None, None)

    
    # Element zoneBasedAccessibility uses Python identifier zoneBasedAccessibility
    __zoneBasedAccessibility = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'zoneBasedAccessibility'), 'zoneBasedAccessibility', '__AbsentNamespace0_matsim4urbansimContolerType_zoneBasedAccessibility', False)

    
    zoneBasedAccessibility = property(__zoneBasedAccessibility.value, __zoneBasedAccessibility.set, None, None)


    _ElementMap = {
        __cellBasedAccessibility.name() : __cellBasedAccessibility,
        __shapeFileCellBasedAccessibility.name() : __shapeFileCellBasedAccessibility,
        __boundingBoxTop.name() : __boundingBoxTop,
        __cellSizeCellBasedAccessibility.name() : __cellSizeCellBasedAccessibility,
        __boundingBoxLeft.name() : __boundingBoxLeft,
        __zone2zoneImpedance.name() : __zone2zoneImpedance,
        __boundingBoxRight.name() : __boundingBoxRight,
        __agentPerformance.name() : __agentPerformance,
        __boundingBoxBottom.name() : __boundingBoxBottom,
        __zoneBasedAccessibility.name() : __zoneBasedAccessibility
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'matsim4urbansimContolerType', matsim4urbansimContolerType)


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


# Complex type configType with content type ELEMENT_ONLY
class configType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'configType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element matsim_config uses Python identifier matsim_config
    __matsim_config = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'matsim_config'), 'matsim_config', '__AbsentNamespace0_configType_matsim_config', False)

    
    matsim_config = property(__matsim_config.value, __matsim_config.set, None, None)

    
    # Element network uses Python identifier network
    __network = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'network'), 'network', '__AbsentNamespace0_configType_network', False)

    
    network = property(__network.value, __network.set, None, None)

    
    # Element inputPlansFile uses Python identifier inputPlansFile
    __inputPlansFile = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'inputPlansFile'), 'inputPlansFile', '__AbsentNamespace0_configType_inputPlansFile', False)

    
    inputPlansFile = property(__inputPlansFile.value, __inputPlansFile.set, None, None)

    
    # Element strategy uses Python identifier strategy
    __strategy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'strategy'), 'strategy', '__AbsentNamespace0_configType_strategy', False)

    
    strategy = property(__strategy.value, __strategy.set, None, None)

    
    # Element hotStartPlansFile uses Python identifier hotStartPlansFile
    __hotStartPlansFile = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'hotStartPlansFile'), 'hotStartPlansFile', '__AbsentNamespace0_configType_hotStartPlansFile', False)

    
    hotStartPlansFile = property(__hotStartPlansFile.value, __hotStartPlansFile.set, None, None)

    
    # Element controler uses Python identifier controler
    __controler = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'controler'), 'controler', '__AbsentNamespace0_configType_controler', False)

    
    controler = property(__controler.value, __controler.set, None, None)

    
    # Element planCalcScore uses Python identifier planCalcScore
    __planCalcScore = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'planCalcScore'), 'planCalcScore', '__AbsentNamespace0_configType_planCalcScore', False)

    
    planCalcScore = property(__planCalcScore.value, __planCalcScore.set, None, None)


    _ElementMap = {
        __matsim_config.name() : __matsim_config,
        __network.name() : __network,
        __inputPlansFile.name() : __inputPlansFile,
        __strategy.name() : __strategy,
        __hotStartPlansFile.name() : __hotStartPlansFile,
        __controler.name() : __controler,
        __planCalcScore.name() : __planCalcScore
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'configType', configType)


matsim_config = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'matsim_config'), matsim_configType)
Namespace.addCategoryObject('elementBinding', matsim_config.name().localName(), matsim_config)



urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'samplingRate'), pyxb.binding.datatypes.double, scope=urbansimParameterType))

urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'matsim4opusConfig'), pyxb.binding.datatypes.token, scope=urbansimParameterType))

urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'year'), pyxb.binding.datatypes.nonNegativeInteger, scope=urbansimParameterType))

urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'opusHome'), pyxb.binding.datatypes.token, scope=urbansimParameterType))

urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'opusDataPath'), pyxb.binding.datatypes.token, scope=urbansimParameterType))

urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'isTestRun'), pyxb.binding.datatypes.boolean, scope=urbansimParameterType))

urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'matsim4opus'), pyxb.binding.datatypes.token, scope=urbansimParameterType))

urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'testParameter'), pyxb.binding.datatypes.token, scope=urbansimParameterType))

urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'matsim4opusOutput'), pyxb.binding.datatypes.token, scope=urbansimParameterType))

urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'backupRunData'), pyxb.binding.datatypes.boolean, scope=urbansimParameterType))

urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'matsim4opusTemp'), pyxb.binding.datatypes.token, scope=urbansimParameterType))
urbansimParameterType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'samplingRate')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'year')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'opusHome')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'opusDataPath')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'matsim4opus')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'matsim4opusConfig')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'matsim4opusOutput')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'matsim4opusTemp')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'isTestRun')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'testParameter')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'backupRunData')), min_occurs=1, max_occurs=1)
    )
urbansimParameterType._ContentModel = pyxb.binding.content.ParticleModel(urbansimParameterType._GroupModel, min_occurs=1, max_occurs=1)



matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'accessibilityParameter'), accessibilityParameterType, scope=matsim4urbansimType))

matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'urbansimParameter'), urbansimParameterType, scope=matsim4urbansimType))

matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'matsim4urbansimContoler'), matsim4urbansimContolerType, scope=matsim4urbansimType))
matsim4urbansimType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, u'urbansimParameter')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, u'matsim4urbansimContoler')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, u'accessibilityParameter')), min_occurs=1L, max_occurs=1L)
    )
matsim4urbansimType._ContentModel = pyxb.binding.content.ParticleModel(matsim4urbansimType._GroupModel, min_occurs=1, max_occurs=1)



accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'useLogitScaleParameterFromMATSim'), pyxb.binding.datatypes.boolean, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'useWalkParameterFromMATSim'), pyxb.binding.datatypes.boolean, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'useRawSumsWithoutLn'), pyxb.binding.datatypes.boolean, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'logitScaleParameter'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'betaCarTravelTimePower2'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'betaCarTravelTime'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'betaWalkLnTravelDistance'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'betaCarLnTravelTime'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'betaCarTravelDistance'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'betaCarTravelDistancePower2'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'betaCarLnTravelDistance'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'betaCarTravelCost'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'betaCarTravelCostPower2'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'betaCarLnTravelCost'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'betaWalkTravelTime'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'betaWalkLnTravelTime'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'betaWalkTravelDistance'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'betaWalkTravelDistancePower2'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'betaWalkTravelTimePower2'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'betaWalkTravelCost'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'betaWalkTravelCostPower2'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'betaWalkLnTravelCost'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'useCarParameterFromMATSim'), pyxb.binding.datatypes.boolean, scope=accessibilityParameterType))
accessibilityParameterType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'useLogitScaleParameterFromMATSim')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'useCarParameterFromMATSim')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'useWalkParameterFromMATSim')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'useRawSumsWithoutLn')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'logitScaleParameter')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'betaCarTravelTime')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'betaCarTravelTimePower2')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'betaCarLnTravelTime')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'betaCarTravelDistance')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'betaCarTravelDistancePower2')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'betaCarLnTravelDistance')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'betaCarTravelCost')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'betaCarTravelCostPower2')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'betaCarLnTravelCost')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'betaWalkTravelTime')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'betaWalkTravelTimePower2')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'betaWalkLnTravelTime')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'betaWalkTravelDistance')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'betaWalkTravelDistancePower2')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'betaWalkLnTravelDistance')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'betaWalkTravelCost')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'betaWalkTravelCostPower2')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'betaWalkLnTravelCost')), min_occurs=1, max_occurs=1)
    )
accessibilityParameterType._ContentModel = pyxb.binding.content.ParticleModel(accessibilityParameterType._GroupModel, min_occurs=1, max_occurs=1)



strategyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'reRouteDijkstraProbability'), pyxb.binding.datatypes.double, scope=strategyType))

strategyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'maxAgentPlanMemorySize'), pyxb.binding.datatypes.nonNegativeInteger, scope=strategyType))

strategyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'changeExpBetaProbability'), pyxb.binding.datatypes.double, scope=strategyType))

strategyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'timeAllocationMutatorProbability'), pyxb.binding.datatypes.double, scope=strategyType))
strategyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(strategyType._UseForTag(pyxb.namespace.ExpandedName(None, u'maxAgentPlanMemorySize')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(strategyType._UseForTag(pyxb.namespace.ExpandedName(None, u'timeAllocationMutatorProbability')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(strategyType._UseForTag(pyxb.namespace.ExpandedName(None, u'changeExpBetaProbability')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(strategyType._UseForTag(pyxb.namespace.ExpandedName(None, u'reRouteDijkstraProbability')), min_occurs=1, max_occurs=1)
    )
strategyType._ContentModel = pyxb.binding.content.ParticleModel(strategyType._GroupModel, min_occurs=1, max_occurs=1)



fileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'inputFile'), pyxb.binding.datatypes.token, scope=fileType))
fileType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(fileType._UseForTag(pyxb.namespace.ExpandedName(None, u'inputFile')), min_occurs=1, max_occurs=1)
    )
fileType._ContentModel = pyxb.binding.content.ParticleModel(fileType._GroupModel, min_occurs=1, max_occurs=1)



inputPlansFileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'inputFile'), pyxb.binding.datatypes.token, scope=inputPlansFileType))
inputPlansFileType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(inputPlansFileType._UseForTag(pyxb.namespace.ExpandedName(None, u'inputFile')), min_occurs=1, max_occurs=1)
    )
inputPlansFileType._ContentModel = pyxb.binding.content.ParticleModel(inputPlansFileType._GroupModel, min_occurs=1, max_occurs=1)



planCalcScoreType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'activityType_0'), pyxb.binding.datatypes.token, scope=planCalcScoreType))

planCalcScoreType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'workActivityLatestStartTime'), pyxb.binding.datatypes.nonNegativeInteger, scope=planCalcScoreType))

planCalcScoreType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'activityType_1'), pyxb.binding.datatypes.token, scope=planCalcScoreType))

planCalcScoreType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'homeActivityTypicalDuration'), pyxb.binding.datatypes.nonNegativeInteger, scope=planCalcScoreType))

planCalcScoreType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'workActivityTypicalDuration'), pyxb.binding.datatypes.nonNegativeInteger, scope=planCalcScoreType))

planCalcScoreType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'workActivityOpeningTime'), pyxb.binding.datatypes.nonNegativeInteger, scope=planCalcScoreType))
planCalcScoreType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(planCalcScoreType._UseForTag(pyxb.namespace.ExpandedName(None, u'activityType_0')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(planCalcScoreType._UseForTag(pyxb.namespace.ExpandedName(None, u'activityType_1')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(planCalcScoreType._UseForTag(pyxb.namespace.ExpandedName(None, u'homeActivityTypicalDuration')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(planCalcScoreType._UseForTag(pyxb.namespace.ExpandedName(None, u'workActivityTypicalDuration')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(planCalcScoreType._UseForTag(pyxb.namespace.ExpandedName(None, u'workActivityOpeningTime')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(planCalcScoreType._UseForTag(pyxb.namespace.ExpandedName(None, u'workActivityLatestStartTime')), min_occurs=1, max_occurs=1)
    )
planCalcScoreType._ContentModel = pyxb.binding.content.ParticleModel(planCalcScoreType._GroupModel, min_occurs=1, max_occurs=1)



matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'matsim4urbansim'), matsim4urbansimType, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'config'), configType, scope=matsim_configType))
matsim_configType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, u'config')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, u'matsim4urbansim')), min_occurs=1L, max_occurs=1L)
    )
matsim_configType._ContentModel = pyxb.binding.content.ParticleModel(matsim_configType._GroupModel, min_occurs=1, max_occurs=1)



matsim4urbansimContolerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'cellBasedAccessibility'), pyxb.binding.datatypes.boolean, scope=matsim4urbansimContolerType))

matsim4urbansimContolerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'shapeFileCellBasedAccessibility'), fileType, scope=matsim4urbansimContolerType))

matsim4urbansimContolerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'boundingBoxTop'), pyxb.binding.datatypes.double, scope=matsim4urbansimContolerType))

matsim4urbansimContolerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'cellSizeCellBasedAccessibility'), pyxb.binding.datatypes.nonNegativeInteger, scope=matsim4urbansimContolerType))

matsim4urbansimContolerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'boundingBoxLeft'), pyxb.binding.datatypes.double, scope=matsim4urbansimContolerType))

matsim4urbansimContolerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'zone2zoneImpedance'), pyxb.binding.datatypes.boolean, scope=matsim4urbansimContolerType))

matsim4urbansimContolerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'boundingBoxRight'), pyxb.binding.datatypes.double, scope=matsim4urbansimContolerType))

matsim4urbansimContolerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'agentPerformance'), pyxb.binding.datatypes.boolean, scope=matsim4urbansimContolerType))

matsim4urbansimContolerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'boundingBoxBottom'), pyxb.binding.datatypes.double, scope=matsim4urbansimContolerType))

matsim4urbansimContolerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'zoneBasedAccessibility'), pyxb.binding.datatypes.boolean, scope=matsim4urbansimContolerType))
matsim4urbansimContolerType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(matsim4urbansimContolerType._UseForTag(pyxb.namespace.ExpandedName(None, u'zone2zoneImpedance')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimContolerType._UseForTag(pyxb.namespace.ExpandedName(None, u'agentPerformance')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimContolerType._UseForTag(pyxb.namespace.ExpandedName(None, u'zoneBasedAccessibility')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimContolerType._UseForTag(pyxb.namespace.ExpandedName(None, u'cellBasedAccessibility')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimContolerType._UseForTag(pyxb.namespace.ExpandedName(None, u'cellSizeCellBasedAccessibility')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimContolerType._UseForTag(pyxb.namespace.ExpandedName(None, u'shapeFileCellBasedAccessibility')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(matsim4urbansimContolerType._UseForTag(pyxb.namespace.ExpandedName(None, u'boundingBoxTop')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimContolerType._UseForTag(pyxb.namespace.ExpandedName(None, u'boundingBoxLeft')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimContolerType._UseForTag(pyxb.namespace.ExpandedName(None, u'boundingBoxRight')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimContolerType._UseForTag(pyxb.namespace.ExpandedName(None, u'boundingBoxBottom')), min_occurs=1, max_occurs=1)
    )
matsim4urbansimContolerType._ContentModel = pyxb.binding.content.ParticleModel(matsim4urbansimContolerType._GroupModel, min_occurs=1, max_occurs=1)



controlerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'lastIteration'), pyxb.binding.datatypes.nonNegativeInteger, scope=controlerType))

controlerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'firstIteration'), pyxb.binding.datatypes.nonNegativeInteger, scope=controlerType))
controlerType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(controlerType._UseForTag(pyxb.namespace.ExpandedName(None, u'firstIteration')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(controlerType._UseForTag(pyxb.namespace.ExpandedName(None, u'lastIteration')), min_occurs=1, max_occurs=1)
    )
controlerType._ContentModel = pyxb.binding.content.ParticleModel(controlerType._GroupModel, min_occurs=1, max_occurs=1)



configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'matsim_config'), fileType, scope=configType))

configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'network'), fileType, scope=configType))

configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'inputPlansFile'), inputPlansFileType, scope=configType))

configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'strategy'), strategyType, scope=configType))

configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'hotStartPlansFile'), inputPlansFileType, scope=configType))

configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'controler'), controlerType, scope=configType))

configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'planCalcScore'), planCalcScoreType, scope=configType))
configType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(configType._UseForTag(pyxb.namespace.ExpandedName(None, u'matsim_config')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(configType._UseForTag(pyxb.namespace.ExpandedName(None, u'network')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(configType._UseForTag(pyxb.namespace.ExpandedName(None, u'inputPlansFile')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(configType._UseForTag(pyxb.namespace.ExpandedName(None, u'hotStartPlansFile')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(configType._UseForTag(pyxb.namespace.ExpandedName(None, u'controler')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(configType._UseForTag(pyxb.namespace.ExpandedName(None, u'planCalcScore')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(configType._UseForTag(pyxb.namespace.ExpandedName(None, u'strategy')), min_occurs=1L, max_occurs=1L)
    )
configType._ContentModel = pyxb.binding.content.ParticleModel(configType._GroupModel, min_occurs=1, max_occurs=1)
