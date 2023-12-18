# Opus/UrbanSim urban simulation software
# Copyright (C) 2010-2012 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

# ./pyxb_matsim_config_parser.py
# PyXB bindings for NM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2013-06-18 11:15:15.096971 by PyXB version 1.1.3
# Namespace AbsentNamespace0

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:95da613d-d7f7-11e2-ae9b-3c07544cd942')

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
    saxer.parse(io.StringIO(xml_text))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, _fallback_namespace=default_namespace)


# Complex type fileType with content type ELEMENT_ONLY
class fileType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'fileType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element inputFile uses Python identifier inputFile
    __inputFile = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'inputFile'), 'inputFile', '__AbsentNamespace0_fileType_inputFile', False)

    
    inputFile = property(__inputFile.value, __inputFile.set, None, None)


    _ElementMap = {
        __inputFile.name() : __inputFile
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', 'fileType', fileType)


# Complex type controlerType with content type ELEMENT_ONLY
class controlerType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'controlerType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element lastIteration uses Python identifier lastIteration
    __lastIteration = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'lastIteration'), 'lastIteration', '__AbsentNamespace0_controlerType_lastIteration', False)

    
    lastIteration = property(__lastIteration.value, __lastIteration.set, None, None)

    
    # Element firstIteration uses Python identifier firstIteration
    __firstIteration = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'firstIteration'), 'firstIteration', '__AbsentNamespace0_controlerType_firstIteration', False)

    
    firstIteration = property(__firstIteration.value, __firstIteration.set, None, None)


    _ElementMap = {
        __lastIteration.name() : __lastIteration,
        __firstIteration.name() : __firstIteration
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', 'controlerType', controlerType)


# Complex type strategyType with content type ELEMENT_ONLY
class strategyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'strategyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element reRouteDijkstraProbability uses Python identifier reRouteDijkstraProbability
    __reRouteDijkstraProbability = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'reRouteDijkstraProbability'), 'reRouteDijkstraProbability', '__AbsentNamespace0_strategyType_reRouteDijkstraProbability', False)

    
    reRouteDijkstraProbability = property(__reRouteDijkstraProbability.value, __reRouteDijkstraProbability.set, None, None)

    
    # Element maxAgentPlanMemorySize uses Python identifier maxAgentPlanMemorySize
    __maxAgentPlanMemorySize = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'maxAgentPlanMemorySize'), 'maxAgentPlanMemorySize', '__AbsentNamespace0_strategyType_maxAgentPlanMemorySize', False)

    
    maxAgentPlanMemorySize = property(__maxAgentPlanMemorySize.value, __maxAgentPlanMemorySize.set, None, None)

    
    # Element changeExpBetaProbability uses Python identifier changeExpBetaProbability
    __changeExpBetaProbability = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'changeExpBetaProbability'), 'changeExpBetaProbability', '__AbsentNamespace0_strategyType_changeExpBetaProbability', False)

    
    changeExpBetaProbability = property(__changeExpBetaProbability.value, __changeExpBetaProbability.set, None, None)

    
    # Element timeAllocationMutatorProbability uses Python identifier timeAllocationMutatorProbability
    __timeAllocationMutatorProbability = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'timeAllocationMutatorProbability'), 'timeAllocationMutatorProbability', '__AbsentNamespace0_strategyType_timeAllocationMutatorProbability', False)

    
    timeAllocationMutatorProbability = property(__timeAllocationMutatorProbability.value, __timeAllocationMutatorProbability.set, None, None)


    _ElementMap = {
        __reRouteDijkstraProbability.name() : __reRouteDijkstraProbability,
        __maxAgentPlanMemorySize.name() : __maxAgentPlanMemorySize,
        __changeExpBetaProbability.name() : __changeExpBetaProbability,
        __timeAllocationMutatorProbability.name() : __timeAllocationMutatorProbability
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', 'strategyType', strategyType)


# Complex type urbansimParameterType with content type ELEMENT_ONLY
class urbansimParameterType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'urbansimParameterType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element urbanSimZoneShapefileLocationDistribution uses Python identifier urbanSimZoneShapefileLocationDistribution
    __urbanSimZoneShapefileLocationDistribution = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'urbanSimZoneShapefileLocationDistribution'), 'urbanSimZoneShapefileLocationDistribution', '__AbsentNamespace0_urbansimParameterType_urbanSimZoneShapefileLocationDistribution', False)

    
    urbanSimZoneShapefileLocationDistribution = property(__urbanSimZoneShapefileLocationDistribution.value, __urbanSimZoneShapefileLocationDistribution.set, None, None)

    
    # Element backupRunData uses Python identifier backupRunData
    __backupRunData = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'backupRunData'), 'backupRunData', '__AbsentNamespace0_urbansimParameterType_backupRunData', False)

    
    backupRunData = property(__backupRunData.value, __backupRunData.set, None, None)

    
    # Element isTestRun uses Python identifier isTestRun
    __isTestRun = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'isTestRun'), 'isTestRun', '__AbsentNamespace0_urbansimParameterType_isTestRun', False)

    
    isTestRun = property(__isTestRun.value, __isTestRun.set, None, None)

    
    # Element matsim4opus uses Python identifier matsim4opus
    __matsim4opus = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'matsim4opus'), 'matsim4opus', '__AbsentNamespace0_urbansimParameterType_matsim4opus', False)

    
    matsim4opus = property(__matsim4opus.value, __matsim4opus.set, None, None)

    
    # Element matsim4opusConfig uses Python identifier matsim4opusConfig
    __matsim4opusConfig = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'matsim4opusConfig'), 'matsim4opusConfig', '__AbsentNamespace0_urbansimParameterType_matsim4opusConfig', False)

    
    matsim4opusConfig = property(__matsim4opusConfig.value, __matsim4opusConfig.set, None, None)

    
    # Element testParameter uses Python identifier testParameter
    __testParameter = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'testParameter'), 'testParameter', '__AbsentNamespace0_urbansimParameterType_testParameter', False)

    
    testParameter = property(__testParameter.value, __testParameter.set, None, None)

    
    # Element opusDataPath uses Python identifier opusDataPath
    __opusDataPath = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'opusDataPath'), 'opusDataPath', '__AbsentNamespace0_urbansimParameterType_opusDataPath', False)

    
    opusDataPath = property(__opusDataPath.value, __opusDataPath.set, None, None)

    
    # Element projectName uses Python identifier projectName
    __projectName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'projectName'), 'projectName', '__AbsentNamespace0_urbansimParameterType_projectName', False)

    
    projectName = property(__projectName.value, __projectName.set, None, None)

    
    # Element matsim4opusTemp uses Python identifier matsim4opusTemp
    __matsim4opusTemp = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'matsim4opusTemp'), 'matsim4opusTemp', '__AbsentNamespace0_urbansimParameterType_matsim4opusTemp', False)

    
    matsim4opusTemp = property(__matsim4opusTemp.value, __matsim4opusTemp.set, None, None)

    
    # Element matsim4opusOutput uses Python identifier matsim4opusOutput
    __matsim4opusOutput = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'matsim4opusOutput'), 'matsim4opusOutput', '__AbsentNamespace0_urbansimParameterType_matsim4opusOutput', False)

    
    matsim4opusOutput = property(__matsim4opusOutput.value, __matsim4opusOutput.set, None, None)

    
    # Element populationSamplingRate uses Python identifier populationSamplingRate
    __populationSamplingRate = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'populationSamplingRate'), 'populationSamplingRate', '__AbsentNamespace0_urbansimParameterType_populationSamplingRate', False)

    
    populationSamplingRate = property(__populationSamplingRate.value, __populationSamplingRate.set, None, None)

    
    # Element useShapefileLocationDistribution uses Python identifier useShapefileLocationDistribution
    __useShapefileLocationDistribution = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'useShapefileLocationDistribution'), 'useShapefileLocationDistribution', '__AbsentNamespace0_urbansimParameterType_useShapefileLocationDistribution', False)

    
    useShapefileLocationDistribution = property(__useShapefileLocationDistribution.value, __useShapefileLocationDistribution.set, None, None)

    
    # Element year uses Python identifier year
    __year = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'year'), 'year', '__AbsentNamespace0_urbansimParameterType_year', False)

    
    year = property(__year.value, __year.set, None, None)

    
    # Element urbanSimZoneRadiusLocationDistribution uses Python identifier urbanSimZoneRadiusLocationDistribution
    __urbanSimZoneRadiusLocationDistribution = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'urbanSimZoneRadiusLocationDistribution'), 'urbanSimZoneRadiusLocationDistribution', '__AbsentNamespace0_urbansimParameterType_urbanSimZoneRadiusLocationDistribution', False)

    
    urbanSimZoneRadiusLocationDistribution = property(__urbanSimZoneRadiusLocationDistribution.value, __urbanSimZoneRadiusLocationDistribution.set, None, None)

    
    # Element opusHome uses Python identifier opusHome
    __opusHome = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'opusHome'), 'opusHome', '__AbsentNamespace0_urbansimParameterType_opusHome', False)

    
    opusHome = property(__opusHome.value, __opusHome.set, None, None)


    _ElementMap = {
        __urbanSimZoneShapefileLocationDistribution.name() : __urbanSimZoneShapefileLocationDistribution,
        __backupRunData.name() : __backupRunData,
        __isTestRun.name() : __isTestRun,
        __matsim4opus.name() : __matsim4opus,
        __matsim4opusConfig.name() : __matsim4opusConfig,
        __testParameter.name() : __testParameter,
        __opusDataPath.name() : __opusDataPath,
        __projectName.name() : __projectName,
        __matsim4opusTemp.name() : __matsim4opusTemp,
        __matsim4opusOutput.name() : __matsim4opusOutput,
        __populationSamplingRate.name() : __populationSamplingRate,
        __useShapefileLocationDistribution.name() : __useShapefileLocationDistribution,
        __year.name() : __year,
        __urbanSimZoneRadiusLocationDistribution.name() : __urbanSimZoneRadiusLocationDistribution,
        __opusHome.name() : __opusHome
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', 'urbansimParameterType', urbansimParameterType)


# Complex type matsim_configType with content type ELEMENT_ONLY
class matsim_configType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'matsim_configType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element matsim4urbansim uses Python identifier matsim4urbansim
    __matsim4urbansim = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'matsim4urbansim'), 'matsim4urbansim', '__AbsentNamespace0_matsim_configType_matsim4urbansim', False)

    
    matsim4urbansim = property(__matsim4urbansim.value, __matsim4urbansim.set, None, None)

    
    # Element config uses Python identifier config
    __config = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'config'), 'config', '__AbsentNamespace0_matsim_configType_config', False)

    
    config = property(__config.value, __config.set, None, None)


    _ElementMap = {
        __matsim4urbansim.name() : __matsim4urbansim,
        __config.name() : __config
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', 'matsim_configType', matsim_configType)


# Complex type inputPlansFileType with content type ELEMENT_ONLY
class inputPlansFileType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'inputPlansFileType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element inputFile uses Python identifier inputFile
    __inputFile = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'inputFile'), 'inputFile', '__AbsentNamespace0_inputPlansFileType_inputFile', False)

    
    inputFile = property(__inputFile.value, __inputFile.set, None, None)


    _ElementMap = {
        __inputFile.name() : __inputFile
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', 'inputPlansFileType', inputPlansFileType)


# Complex type accessibilityParameterType with content type ELEMENT_ONLY
class accessibilityParameterType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'accessibilityParameterType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element betaCarTravelCost uses Python identifier betaCarTravelCost
    __betaCarTravelCost = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'betaCarTravelCost'), 'betaCarTravelCost', '__AbsentNamespace0_accessibilityParameterType_betaCarTravelCost', False)

    
    betaCarTravelCost = property(__betaCarTravelCost.value, __betaCarTravelCost.set, None, None)

    
    # Element betaCarTravelCostPower2 uses Python identifier betaCarTravelCostPower2
    __betaCarTravelCostPower2 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'betaCarTravelCostPower2'), 'betaCarTravelCostPower2', '__AbsentNamespace0_accessibilityParameterType_betaCarTravelCostPower2', False)

    
    betaCarTravelCostPower2 = property(__betaCarTravelCostPower2.value, __betaCarTravelCostPower2.set, None, None)

    
    # Element betaBikeTravelTime uses Python identifier betaBikeTravelTime
    __betaBikeTravelTime = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'betaBikeTravelTime'), 'betaBikeTravelTime', '__AbsentNamespace0_accessibilityParameterType_betaBikeTravelTime', False)

    
    betaBikeTravelTime = property(__betaBikeTravelTime.value, __betaBikeTravelTime.set, None, None)

    
    # Element betaCarLnTravelCost uses Python identifier betaCarLnTravelCost
    __betaCarLnTravelCost = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'betaCarLnTravelCost'), 'betaCarLnTravelCost', '__AbsentNamespace0_accessibilityParameterType_betaCarLnTravelCost', False)

    
    betaCarLnTravelCost = property(__betaCarLnTravelCost.value, __betaCarLnTravelCost.set, None, None)

    
    # Element betaBikeTravelTimePower2 uses Python identifier betaBikeTravelTimePower2
    __betaBikeTravelTimePower2 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'betaBikeTravelTimePower2'), 'betaBikeTravelTimePower2', '__AbsentNamespace0_accessibilityParameterType_betaBikeTravelTimePower2', False)

    
    betaBikeTravelTimePower2 = property(__betaBikeTravelTimePower2.value, __betaBikeTravelTimePower2.set, None, None)

    
    # Element betaBikeLnTravelTime uses Python identifier betaBikeLnTravelTime
    __betaBikeLnTravelTime = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'betaBikeLnTravelTime'), 'betaBikeLnTravelTime', '__AbsentNamespace0_accessibilityParameterType_betaBikeLnTravelTime', False)

    
    betaBikeLnTravelTime = property(__betaBikeLnTravelTime.value, __betaBikeLnTravelTime.set, None, None)

    
    # Element betaBikeTravelDistance uses Python identifier betaBikeTravelDistance
    __betaBikeTravelDistance = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'betaBikeTravelDistance'), 'betaBikeTravelDistance', '__AbsentNamespace0_accessibilityParameterType_betaBikeTravelDistance', False)

    
    betaBikeTravelDistance = property(__betaBikeTravelDistance.value, __betaBikeTravelDistance.set, None, None)

    
    # Element betaBikeTravelDistancePower2 uses Python identifier betaBikeTravelDistancePower2
    __betaBikeTravelDistancePower2 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'betaBikeTravelDistancePower2'), 'betaBikeTravelDistancePower2', '__AbsentNamespace0_accessibilityParameterType_betaBikeTravelDistancePower2', False)

    
    betaBikeTravelDistancePower2 = property(__betaBikeTravelDistancePower2.value, __betaBikeTravelDistancePower2.set, None, None)

    
    # Element betaBikeTravelCost uses Python identifier betaBikeTravelCost
    __betaBikeTravelCost = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'betaBikeTravelCost'), 'betaBikeTravelCost', '__AbsentNamespace0_accessibilityParameterType_betaBikeTravelCost', False)

    
    betaBikeTravelCost = property(__betaBikeTravelCost.value, __betaBikeTravelCost.set, None, None)

    
    # Element betaBikeTravelCostPower2 uses Python identifier betaBikeTravelCostPower2
    __betaBikeTravelCostPower2 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'betaBikeTravelCostPower2'), 'betaBikeTravelCostPower2', '__AbsentNamespace0_accessibilityParameterType_betaBikeTravelCostPower2', False)

    
    betaBikeTravelCostPower2 = property(__betaBikeTravelCostPower2.value, __betaBikeTravelCostPower2.set, None, None)

    
    # Element betaBikeLnTravelCost uses Python identifier betaBikeLnTravelCost
    __betaBikeLnTravelCost = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'betaBikeLnTravelCost'), 'betaBikeLnTravelCost', '__AbsentNamespace0_accessibilityParameterType_betaBikeLnTravelCost', False)

    
    betaBikeLnTravelCost = property(__betaBikeLnTravelCost.value, __betaBikeLnTravelCost.set, None, None)

    
    # Element betaWalkTravelTime uses Python identifier betaWalkTravelTime
    __betaWalkTravelTime = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'betaWalkTravelTime'), 'betaWalkTravelTime', '__AbsentNamespace0_accessibilityParameterType_betaWalkTravelTime', False)

    
    betaWalkTravelTime = property(__betaWalkTravelTime.value, __betaWalkTravelTime.set, None, None)

    
    # Element betaWalkTravelTimePower2 uses Python identifier betaWalkTravelTimePower2
    __betaWalkTravelTimePower2 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'betaWalkTravelTimePower2'), 'betaWalkTravelTimePower2', '__AbsentNamespace0_accessibilityParameterType_betaWalkTravelTimePower2', False)

    
    betaWalkTravelTimePower2 = property(__betaWalkTravelTimePower2.value, __betaWalkTravelTimePower2.set, None, None)

    
    # Element betaWalkLnTravelTime uses Python identifier betaWalkLnTravelTime
    __betaWalkLnTravelTime = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'betaWalkLnTravelTime'), 'betaWalkLnTravelTime', '__AbsentNamespace0_accessibilityParameterType_betaWalkLnTravelTime', False)

    
    betaWalkLnTravelTime = property(__betaWalkLnTravelTime.value, __betaWalkLnTravelTime.set, None, None)

    
    # Element betaWalkTravelDistance uses Python identifier betaWalkTravelDistance
    __betaWalkTravelDistance = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'betaWalkTravelDistance'), 'betaWalkTravelDistance', '__AbsentNamespace0_accessibilityParameterType_betaWalkTravelDistance', False)

    
    betaWalkTravelDistance = property(__betaWalkTravelDistance.value, __betaWalkTravelDistance.set, None, None)

    
    # Element betaWalkTravelDistancePower2 uses Python identifier betaWalkTravelDistancePower2
    __betaWalkTravelDistancePower2 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'betaWalkTravelDistancePower2'), 'betaWalkTravelDistancePower2', '__AbsentNamespace0_accessibilityParameterType_betaWalkTravelDistancePower2', False)

    
    betaWalkTravelDistancePower2 = property(__betaWalkTravelDistancePower2.value, __betaWalkTravelDistancePower2.set, None, None)

    
    # Element betaWalkLnTravelDistance uses Python identifier betaWalkLnTravelDistance
    __betaWalkLnTravelDistance = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'betaWalkLnTravelDistance'), 'betaWalkLnTravelDistance', '__AbsentNamespace0_accessibilityParameterType_betaWalkLnTravelDistance', False)

    
    betaWalkLnTravelDistance = property(__betaWalkLnTravelDistance.value, __betaWalkLnTravelDistance.set, None, None)

    
    # Element betaWalkTravelCost uses Python identifier betaWalkTravelCost
    __betaWalkTravelCost = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'betaWalkTravelCost'), 'betaWalkTravelCost', '__AbsentNamespace0_accessibilityParameterType_betaWalkTravelCost', False)

    
    betaWalkTravelCost = property(__betaWalkTravelCost.value, __betaWalkTravelCost.set, None, None)

    
    # Element betaWalkTravelCostPower2 uses Python identifier betaWalkTravelCostPower2
    __betaWalkTravelCostPower2 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'betaWalkTravelCostPower2'), 'betaWalkTravelCostPower2', '__AbsentNamespace0_accessibilityParameterType_betaWalkTravelCostPower2', False)

    
    betaWalkTravelCostPower2 = property(__betaWalkTravelCostPower2.value, __betaWalkTravelCostPower2.set, None, None)

    
    # Element opportunitiySamplingRate uses Python identifier opportunitiySamplingRate
    __opportunitiySamplingRate = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'opportunitiySamplingRate'), 'opportunitiySamplingRate', '__AbsentNamespace0_accessibilityParameterType_opportunitiySamplingRate', False)

    
    opportunitiySamplingRate = property(__opportunitiySamplingRate.value, __opportunitiySamplingRate.set, None, None)

    
    # Element betaWalkLnTravelCost uses Python identifier betaWalkLnTravelCost
    __betaWalkLnTravelCost = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'betaWalkLnTravelCost'), 'betaWalkLnTravelCost', '__AbsentNamespace0_accessibilityParameterType_betaWalkLnTravelCost', False)

    
    betaWalkLnTravelCost = property(__betaWalkLnTravelCost.value, __betaWalkLnTravelCost.set, None, None)

    
    # Element useCarParameterFromMATSim uses Python identifier useCarParameterFromMATSim
    __useCarParameterFromMATSim = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'useCarParameterFromMATSim'), 'useCarParameterFromMATSim', '__AbsentNamespace0_accessibilityParameterType_useCarParameterFromMATSim', False)

    
    useCarParameterFromMATSim = property(__useCarParameterFromMATSim.value, __useCarParameterFromMATSim.set, None, None)

    
    # Element useBikeParameterFromMATSim uses Python identifier useBikeParameterFromMATSim
    __useBikeParameterFromMATSim = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'useBikeParameterFromMATSim'), 'useBikeParameterFromMATSim', '__AbsentNamespace0_accessibilityParameterType_useBikeParameterFromMATSim', False)

    
    useBikeParameterFromMATSim = property(__useBikeParameterFromMATSim.value, __useBikeParameterFromMATSim.set, None, None)

    
    # Element useLogitScaleParameterFromMATSim uses Python identifier useLogitScaleParameterFromMATSim
    __useLogitScaleParameterFromMATSim = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'useLogitScaleParameterFromMATSim'), 'useLogitScaleParameterFromMATSim', '__AbsentNamespace0_accessibilityParameterType_useLogitScaleParameterFromMATSim', False)

    
    useLogitScaleParameterFromMATSim = property(__useLogitScaleParameterFromMATSim.value, __useLogitScaleParameterFromMATSim.set, None, None)

    
    # Element useWalkParameterFromMATSim uses Python identifier useWalkParameterFromMATSim
    __useWalkParameterFromMATSim = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'useWalkParameterFromMATSim'), 'useWalkParameterFromMATSim', '__AbsentNamespace0_accessibilityParameterType_useWalkParameterFromMATSim', False)

    
    useWalkParameterFromMATSim = property(__useWalkParameterFromMATSim.value, __useWalkParameterFromMATSim.set, None, None)

    
    # Element useRawSumsWithoutLn uses Python identifier useRawSumsWithoutLn
    __useRawSumsWithoutLn = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'useRawSumsWithoutLn'), 'useRawSumsWithoutLn', '__AbsentNamespace0_accessibilityParameterType_useRawSumsWithoutLn', False)

    
    useRawSumsWithoutLn = property(__useRawSumsWithoutLn.value, __useRawSumsWithoutLn.set, None, None)

    
    # Element betaBikeLnTravelDistance uses Python identifier betaBikeLnTravelDistance
    __betaBikeLnTravelDistance = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'betaBikeLnTravelDistance'), 'betaBikeLnTravelDistance', '__AbsentNamespace0_accessibilityParameterType_betaBikeLnTravelDistance', False)

    
    betaBikeLnTravelDistance = property(__betaBikeLnTravelDistance.value, __betaBikeLnTravelDistance.set, None, None)

    
    # Element logitScaleParameter uses Python identifier logitScaleParameter
    __logitScaleParameter = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'logitScaleParameter'), 'logitScaleParameter', '__AbsentNamespace0_accessibilityParameterType_logitScaleParameter', False)

    
    logitScaleParameter = property(__logitScaleParameter.value, __logitScaleParameter.set, None, None)

    
    # Element betaCarTravelTime uses Python identifier betaCarTravelTime
    __betaCarTravelTime = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'betaCarTravelTime'), 'betaCarTravelTime', '__AbsentNamespace0_accessibilityParameterType_betaCarTravelTime', False)

    
    betaCarTravelTime = property(__betaCarTravelTime.value, __betaCarTravelTime.set, None, None)

    
    # Element betaCarTravelTimePower2 uses Python identifier betaCarTravelTimePower2
    __betaCarTravelTimePower2 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'betaCarTravelTimePower2'), 'betaCarTravelTimePower2', '__AbsentNamespace0_accessibilityParameterType_betaCarTravelTimePower2', False)

    
    betaCarTravelTimePower2 = property(__betaCarTravelTimePower2.value, __betaCarTravelTimePower2.set, None, None)

    
    # Element betaCarLnTravelTime uses Python identifier betaCarLnTravelTime
    __betaCarLnTravelTime = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'betaCarLnTravelTime'), 'betaCarLnTravelTime', '__AbsentNamespace0_accessibilityParameterType_betaCarLnTravelTime', False)

    
    betaCarLnTravelTime = property(__betaCarLnTravelTime.value, __betaCarLnTravelTime.set, None, None)

    
    # Element betaCarTravelDistance uses Python identifier betaCarTravelDistance
    __betaCarTravelDistance = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'betaCarTravelDistance'), 'betaCarTravelDistance', '__AbsentNamespace0_accessibilityParameterType_betaCarTravelDistance', False)

    
    betaCarTravelDistance = property(__betaCarTravelDistance.value, __betaCarTravelDistance.set, None, None)

    
    # Element betaCarTravelDistancePower2 uses Python identifier betaCarTravelDistancePower2
    __betaCarTravelDistancePower2 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'betaCarTravelDistancePower2'), 'betaCarTravelDistancePower2', '__AbsentNamespace0_accessibilityParameterType_betaCarTravelDistancePower2', False)

    
    betaCarTravelDistancePower2 = property(__betaCarTravelDistancePower2.value, __betaCarTravelDistancePower2.set, None, None)

    
    # Element betaCarLnTravelDistance uses Python identifier betaCarLnTravelDistance
    __betaCarLnTravelDistance = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'betaCarLnTravelDistance'), 'betaCarLnTravelDistance', '__AbsentNamespace0_accessibilityParameterType_betaCarLnTravelDistance', False)

    
    betaCarLnTravelDistance = property(__betaCarLnTravelDistance.value, __betaCarLnTravelDistance.set, None, None)


    _ElementMap = {
        __betaCarTravelCost.name() : __betaCarTravelCost,
        __betaCarTravelCostPower2.name() : __betaCarTravelCostPower2,
        __betaBikeTravelTime.name() : __betaBikeTravelTime,
        __betaCarLnTravelCost.name() : __betaCarLnTravelCost,
        __betaBikeTravelTimePower2.name() : __betaBikeTravelTimePower2,
        __betaBikeLnTravelTime.name() : __betaBikeLnTravelTime,
        __betaBikeTravelDistance.name() : __betaBikeTravelDistance,
        __betaBikeTravelDistancePower2.name() : __betaBikeTravelDistancePower2,
        __betaBikeTravelCost.name() : __betaBikeTravelCost,
        __betaBikeTravelCostPower2.name() : __betaBikeTravelCostPower2,
        __betaBikeLnTravelCost.name() : __betaBikeLnTravelCost,
        __betaWalkTravelTime.name() : __betaWalkTravelTime,
        __betaWalkTravelTimePower2.name() : __betaWalkTravelTimePower2,
        __betaWalkLnTravelTime.name() : __betaWalkLnTravelTime,
        __betaWalkTravelDistance.name() : __betaWalkTravelDistance,
        __betaWalkTravelDistancePower2.name() : __betaWalkTravelDistancePower2,
        __betaWalkLnTravelDistance.name() : __betaWalkLnTravelDistance,
        __betaWalkTravelCost.name() : __betaWalkTravelCost,
        __betaWalkTravelCostPower2.name() : __betaWalkTravelCostPower2,
        __opportunitiySamplingRate.name() : __opportunitiySamplingRate,
        __betaWalkLnTravelCost.name() : __betaWalkLnTravelCost,
        __useCarParameterFromMATSim.name() : __useCarParameterFromMATSim,
        __useBikeParameterFromMATSim.name() : __useBikeParameterFromMATSim,
        __useLogitScaleParameterFromMATSim.name() : __useLogitScaleParameterFromMATSim,
        __useWalkParameterFromMATSim.name() : __useWalkParameterFromMATSim,
        __useRawSumsWithoutLn.name() : __useRawSumsWithoutLn,
        __betaBikeLnTravelDistance.name() : __betaBikeLnTravelDistance,
        __logitScaleParameter.name() : __logitScaleParameter,
        __betaCarTravelTime.name() : __betaCarTravelTime,
        __betaCarTravelTimePower2.name() : __betaCarTravelTimePower2,
        __betaCarLnTravelTime.name() : __betaCarLnTravelTime,
        __betaCarTravelDistance.name() : __betaCarTravelDistance,
        __betaCarTravelDistancePower2.name() : __betaCarTravelDistancePower2,
        __betaCarLnTravelDistance.name() : __betaCarLnTravelDistance
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', 'accessibilityParameterType', accessibilityParameterType)


# Complex type planCalcScoreType with content type ELEMENT_ONLY
class planCalcScoreType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'planCalcScoreType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element homeActivityTypicalDuration uses Python identifier homeActivityTypicalDuration
    __homeActivityTypicalDuration = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'homeActivityTypicalDuration'), 'homeActivityTypicalDuration', '__AbsentNamespace0_planCalcScoreType_homeActivityTypicalDuration', False)

    
    homeActivityTypicalDuration = property(__homeActivityTypicalDuration.value, __homeActivityTypicalDuration.set, None, None)

    
    # Element workActivityTypicalDuration uses Python identifier workActivityTypicalDuration
    __workActivityTypicalDuration = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'workActivityTypicalDuration'), 'workActivityTypicalDuration', '__AbsentNamespace0_planCalcScoreType_workActivityTypicalDuration', False)

    
    workActivityTypicalDuration = property(__workActivityTypicalDuration.value, __workActivityTypicalDuration.set, None, None)

    
    # Element workActivityOpeningTime uses Python identifier workActivityOpeningTime
    __workActivityOpeningTime = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'workActivityOpeningTime'), 'workActivityOpeningTime', '__AbsentNamespace0_planCalcScoreType_workActivityOpeningTime', False)

    
    workActivityOpeningTime = property(__workActivityOpeningTime.value, __workActivityOpeningTime.set, None, None)

    
    # Element activityType_1 uses Python identifier activityType_1
    __activityType_1 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'activityType_1'), 'activityType_1', '__AbsentNamespace0_planCalcScoreType_activityType_1', False)

    
    activityType_1 = property(__activityType_1.value, __activityType_1.set, None, None)

    
    # Element workActivityLatestStartTime uses Python identifier workActivityLatestStartTime
    __workActivityLatestStartTime = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'workActivityLatestStartTime'), 'workActivityLatestStartTime', '__AbsentNamespace0_planCalcScoreType_workActivityLatestStartTime', False)

    
    workActivityLatestStartTime = property(__workActivityLatestStartTime.value, __workActivityLatestStartTime.set, None, None)

    
    # Element activityType_0 uses Python identifier activityType_0
    __activityType_0 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'activityType_0'), 'activityType_0', '__AbsentNamespace0_planCalcScoreType_activityType_0', False)

    
    activityType_0 = property(__activityType_0.value, __activityType_0.set, None, None)


    _ElementMap = {
        __homeActivityTypicalDuration.name() : __homeActivityTypicalDuration,
        __workActivityTypicalDuration.name() : __workActivityTypicalDuration,
        __workActivityOpeningTime.name() : __workActivityOpeningTime,
        __activityType_1.name() : __activityType_1,
        __workActivityLatestStartTime.name() : __workActivityLatestStartTime,
        __activityType_0.name() : __activityType_0
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', 'planCalcScoreType', planCalcScoreType)


# Complex type matsim4urbansimContolerType with content type ELEMENT_ONLY
class matsim4urbansimContolerType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'matsim4urbansimContolerType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element cellSizeCellBasedAccessibility uses Python identifier cellSizeCellBasedAccessibility
    __cellSizeCellBasedAccessibility = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'cellSizeCellBasedAccessibility'), 'cellSizeCellBasedAccessibility', '__AbsentNamespace0_matsim4urbansimContolerType_cellSizeCellBasedAccessibility', False)

    
    cellSizeCellBasedAccessibility = property(__cellSizeCellBasedAccessibility.value, __cellSizeCellBasedAccessibility.set, None, None)

    
    # Element cellBasedAccessibility uses Python identifier cellBasedAccessibility
    __cellBasedAccessibility = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'cellBasedAccessibility'), 'cellBasedAccessibility', '__AbsentNamespace0_matsim4urbansimContolerType_cellBasedAccessibility', False)

    
    cellBasedAccessibility = property(__cellBasedAccessibility.value, __cellBasedAccessibility.set, None, None)

    
    # Element agentPerformance uses Python identifier agentPerformance
    __agentPerformance = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'agentPerformance'), 'agentPerformance', '__AbsentNamespace0_matsim4urbansimContolerType_agentPerformance', False)

    
    agentPerformance = property(__agentPerformance.value, __agentPerformance.set, None, None)

    
    # Element shapeFileCellBasedAccessibility uses Python identifier shapeFileCellBasedAccessibility
    __shapeFileCellBasedAccessibility = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'shapeFileCellBasedAccessibility'), 'shapeFileCellBasedAccessibility', '__AbsentNamespace0_matsim4urbansimContolerType_shapeFileCellBasedAccessibility', False)

    
    shapeFileCellBasedAccessibility = property(__shapeFileCellBasedAccessibility.value, __shapeFileCellBasedAccessibility.set, None, None)

    
    # Element useCustomBoundingBox uses Python identifier useCustomBoundingBox
    __useCustomBoundingBox = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'useCustomBoundingBox'), 'useCustomBoundingBox', '__AbsentNamespace0_matsim4urbansimContolerType_useCustomBoundingBox', False)

    
    useCustomBoundingBox = property(__useCustomBoundingBox.value, __useCustomBoundingBox.set, None, None)

    
    # Element timeOfADay uses Python identifier timeOfADay
    __timeOfADay = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'timeOfADay'), 'timeOfADay', '__AbsentNamespace0_matsim4urbansimContolerType_timeOfADay', False)

    
    timeOfADay = property(__timeOfADay.value, __timeOfADay.set, None, None)

    
    # Element boundingBoxTop uses Python identifier boundingBoxTop
    __boundingBoxTop = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'boundingBoxTop'), 'boundingBoxTop', '__AbsentNamespace0_matsim4urbansimContolerType_boundingBoxTop', False)

    
    boundingBoxTop = property(__boundingBoxTop.value, __boundingBoxTop.set, None, None)

    
    # Element boundingBoxLeft uses Python identifier boundingBoxLeft
    __boundingBoxLeft = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'boundingBoxLeft'), 'boundingBoxLeft', '__AbsentNamespace0_matsim4urbansimContolerType_boundingBoxLeft', False)

    
    boundingBoxLeft = property(__boundingBoxLeft.value, __boundingBoxLeft.set, None, None)

    
    # Element zone2zoneImpedance uses Python identifier zone2zoneImpedance
    __zone2zoneImpedance = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'zone2zoneImpedance'), 'zone2zoneImpedance', '__AbsentNamespace0_matsim4urbansimContolerType_zone2zoneImpedance', False)

    
    zone2zoneImpedance = property(__zone2zoneImpedance.value, __zone2zoneImpedance.set, None, None)

    
    # Element boundingBoxRight uses Python identifier boundingBoxRight
    __boundingBoxRight = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'boundingBoxRight'), 'boundingBoxRight', '__AbsentNamespace0_matsim4urbansimContolerType_boundingBoxRight', False)

    
    boundingBoxRight = property(__boundingBoxRight.value, __boundingBoxRight.set, None, None)

    
    # Element boundingBoxBottom uses Python identifier boundingBoxBottom
    __boundingBoxBottom = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'boundingBoxBottom'), 'boundingBoxBottom', '__AbsentNamespace0_matsim4urbansimContolerType_boundingBoxBottom', False)

    
    boundingBoxBottom = property(__boundingBoxBottom.value, __boundingBoxBottom.set, None, None)

    
    # Element zoneBasedAccessibility uses Python identifier zoneBasedAccessibility
    __zoneBasedAccessibility = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'zoneBasedAccessibility'), 'zoneBasedAccessibility', '__AbsentNamespace0_matsim4urbansimContolerType_zoneBasedAccessibility', False)

    
    zoneBasedAccessibility = property(__zoneBasedAccessibility.value, __zoneBasedAccessibility.set, None, None)


    _ElementMap = {
        __cellSizeCellBasedAccessibility.name() : __cellSizeCellBasedAccessibility,
        __cellBasedAccessibility.name() : __cellBasedAccessibility,
        __agentPerformance.name() : __agentPerformance,
        __shapeFileCellBasedAccessibility.name() : __shapeFileCellBasedAccessibility,
        __useCustomBoundingBox.name() : __useCustomBoundingBox,
        __timeOfADay.name() : __timeOfADay,
        __boundingBoxTop.name() : __boundingBoxTop,
        __boundingBoxLeft.name() : __boundingBoxLeft,
        __zone2zoneImpedance.name() : __zone2zoneImpedance,
        __boundingBoxRight.name() : __boundingBoxRight,
        __boundingBoxBottom.name() : __boundingBoxBottom,
        __zoneBasedAccessibility.name() : __zoneBasedAccessibility
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', 'matsim4urbansimContolerType', matsim4urbansimContolerType)


# Complex type configType with content type ELEMENT_ONLY
class configType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'configType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element inputPlansFile uses Python identifier inputPlansFile
    __inputPlansFile = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'inputPlansFile'), 'inputPlansFile', '__AbsentNamespace0_configType_inputPlansFile', False)

    
    inputPlansFile = property(__inputPlansFile.value, __inputPlansFile.set, None, None)

    
    # Element controler uses Python identifier controler
    __controler = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'controler'), 'controler', '__AbsentNamespace0_configType_controler', False)

    
    controler = property(__controler.value, __controler.set, None, None)

    
    # Element planCalcScore uses Python identifier planCalcScore
    __planCalcScore = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'planCalcScore'), 'planCalcScore', '__AbsentNamespace0_configType_planCalcScore', False)

    
    planCalcScore = property(__planCalcScore.value, __planCalcScore.set, None, None)

    
    # Element hotStartPlansFile uses Python identifier hotStartPlansFile
    __hotStartPlansFile = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'hotStartPlansFile'), 'hotStartPlansFile', '__AbsentNamespace0_configType_hotStartPlansFile', False)

    
    hotStartPlansFile = property(__hotStartPlansFile.value, __hotStartPlansFile.set, None, None)

    
    # Element strategy uses Python identifier strategy
    __strategy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'strategy'), 'strategy', '__AbsentNamespace0_configType_strategy', False)

    
    strategy = property(__strategy.value, __strategy.set, None, None)

    
    # Element matsim_config uses Python identifier matsim_config
    __matsim_config = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'matsim_config'), 'matsim_config', '__AbsentNamespace0_configType_matsim_config', False)

    
    matsim_config = property(__matsim_config.value, __matsim_config.set, None, None)

    
    # Element network uses Python identifier network
    __network = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'network'), 'network', '__AbsentNamespace0_configType_network', False)

    
    network = property(__network.value, __network.set, None, None)


    _ElementMap = {
        __inputPlansFile.name() : __inputPlansFile,
        __controler.name() : __controler,
        __planCalcScore.name() : __planCalcScore,
        __hotStartPlansFile.name() : __hotStartPlansFile,
        __strategy.name() : __strategy,
        __matsim_config.name() : __matsim_config,
        __network.name() : __network
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', 'configType', configType)


# Complex type matsim4urbansimType with content type ELEMENT_ONLY
class matsim4urbansimType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'matsim4urbansimType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element accessibilityParameter uses Python identifier accessibilityParameter
    __accessibilityParameter = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'accessibilityParameter'), 'accessibilityParameter', '__AbsentNamespace0_matsim4urbansimType_accessibilityParameter', False)

    
    accessibilityParameter = property(__accessibilityParameter.value, __accessibilityParameter.set, None, None)

    
    # Element urbansimParameter uses Python identifier urbansimParameter
    __urbansimParameter = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'urbansimParameter'), 'urbansimParameter', '__AbsentNamespace0_matsim4urbansimType_urbansimParameter', False)

    
    urbansimParameter = property(__urbansimParameter.value, __urbansimParameter.set, None, None)

    
    # Element matsim4urbansimContoler uses Python identifier matsim4urbansimContoler
    __matsim4urbansimContoler = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'matsim4urbansimContoler'), 'matsim4urbansimContoler', '__AbsentNamespace0_matsim4urbansimType_matsim4urbansimContoler', False)

    
    matsim4urbansimContoler = property(__matsim4urbansimContoler.value, __matsim4urbansimContoler.set, None, None)


    _ElementMap = {
        __accessibilityParameter.name() : __accessibilityParameter,
        __urbansimParameter.name() : __urbansimParameter,
        __matsim4urbansimContoler.name() : __matsim4urbansimContoler
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', 'matsim4urbansimType', matsim4urbansimType)


matsim_config = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'matsim_config'), matsim_configType)
Namespace.addCategoryObject('elementBinding', matsim_config.name().localName(), matsim_config)



fileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'inputFile'), pyxb.binding.datatypes.token, scope=fileType))
fileType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(fileType._UseForTag(pyxb.namespace.ExpandedName(None, 'inputFile')), min_occurs=1, max_occurs=1)
    )
fileType._ContentModel = pyxb.binding.content.ParticleModel(fileType._GroupModel, min_occurs=1, max_occurs=1)



controlerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'lastIteration'), pyxb.binding.datatypes.nonNegativeInteger, scope=controlerType))

controlerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'firstIteration'), pyxb.binding.datatypes.nonNegativeInteger, scope=controlerType))
controlerType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(controlerType._UseForTag(pyxb.namespace.ExpandedName(None, 'firstIteration')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(controlerType._UseForTag(pyxb.namespace.ExpandedName(None, 'lastIteration')), min_occurs=1, max_occurs=1)
    )
controlerType._ContentModel = pyxb.binding.content.ParticleModel(controlerType._GroupModel, min_occurs=1, max_occurs=1)



strategyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'reRouteDijkstraProbability'), pyxb.binding.datatypes.double, scope=strategyType))

strategyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'maxAgentPlanMemorySize'), pyxb.binding.datatypes.nonNegativeInteger, scope=strategyType))

strategyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'changeExpBetaProbability'), pyxb.binding.datatypes.double, scope=strategyType))

strategyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'timeAllocationMutatorProbability'), pyxb.binding.datatypes.double, scope=strategyType))
strategyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(strategyType._UseForTag(pyxb.namespace.ExpandedName(None, 'maxAgentPlanMemorySize')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(strategyType._UseForTag(pyxb.namespace.ExpandedName(None, 'timeAllocationMutatorProbability')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(strategyType._UseForTag(pyxb.namespace.ExpandedName(None, 'changeExpBetaProbability')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(strategyType._UseForTag(pyxb.namespace.ExpandedName(None, 'reRouteDijkstraProbability')), min_occurs=1, max_occurs=1)
    )
strategyType._ContentModel = pyxb.binding.content.ParticleModel(strategyType._GroupModel, min_occurs=1, max_occurs=1)



urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'urbanSimZoneShapefileLocationDistribution'), fileType, scope=urbansimParameterType))

urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'backupRunData'), pyxb.binding.datatypes.boolean, scope=urbansimParameterType))

urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'isTestRun'), pyxb.binding.datatypes.boolean, scope=urbansimParameterType))

urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'matsim4opus'), pyxb.binding.datatypes.token, scope=urbansimParameterType))

urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'matsim4opusConfig'), pyxb.binding.datatypes.token, scope=urbansimParameterType))

urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'testParameter'), pyxb.binding.datatypes.token, scope=urbansimParameterType))

urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'opusDataPath'), pyxb.binding.datatypes.token, scope=urbansimParameterType))

urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'projectName'), pyxb.binding.datatypes.token, scope=urbansimParameterType))

urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'matsim4opusTemp'), pyxb.binding.datatypes.token, scope=urbansimParameterType))

urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'matsim4opusOutput'), pyxb.binding.datatypes.token, scope=urbansimParameterType))

urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'populationSamplingRate'), pyxb.binding.datatypes.double, scope=urbansimParameterType))

urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'useShapefileLocationDistribution'), pyxb.binding.datatypes.boolean, scope=urbansimParameterType))

urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'year'), pyxb.binding.datatypes.nonNegativeInteger, scope=urbansimParameterType))

urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'urbanSimZoneRadiusLocationDistribution'), pyxb.binding.datatypes.double, scope=urbansimParameterType))

urbansimParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'opusHome'), pyxb.binding.datatypes.token, scope=urbansimParameterType))
urbansimParameterType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'projectName')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'populationSamplingRate')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'year')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'opusHome')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'opusDataPath')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'matsim4opus')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'matsim4opusConfig')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'matsim4opusOutput')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'matsim4opusTemp')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'useShapefileLocationDistribution')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'urbanSimZoneRadiusLocationDistribution')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'urbanSimZoneShapefileLocationDistribution')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'isTestRun')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'testParameter')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(urbansimParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'backupRunData')), min_occurs=1, max_occurs=1)
    )
urbansimParameterType._ContentModel = pyxb.binding.content.ParticleModel(urbansimParameterType._GroupModel, min_occurs=1, max_occurs=1)



matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'matsim4urbansim'), matsim4urbansimType, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'config'), configType, scope=matsim_configType))
matsim_configType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, 'config')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, 'matsim4urbansim')), min_occurs=1, max_occurs=1)
    )
matsim_configType._ContentModel = pyxb.binding.content.ParticleModel(matsim_configType._GroupModel, min_occurs=1, max_occurs=1)



inputPlansFileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'inputFile'), pyxb.binding.datatypes.token, scope=inputPlansFileType))
inputPlansFileType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(inputPlansFileType._UseForTag(pyxb.namespace.ExpandedName(None, 'inputFile')), min_occurs=1, max_occurs=1)
    )
inputPlansFileType._ContentModel = pyxb.binding.content.ParticleModel(inputPlansFileType._GroupModel, min_occurs=1, max_occurs=1)



accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'betaCarTravelCost'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'betaCarTravelCostPower2'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'betaBikeTravelTime'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'betaCarLnTravelCost'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'betaBikeTravelTimePower2'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'betaBikeLnTravelTime'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'betaBikeTravelDistance'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'betaBikeTravelDistancePower2'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'betaBikeTravelCost'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'betaBikeTravelCostPower2'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'betaBikeLnTravelCost'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'betaWalkTravelTime'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'betaWalkTravelTimePower2'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'betaWalkLnTravelTime'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'betaWalkTravelDistance'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'betaWalkTravelDistancePower2'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'betaWalkLnTravelDistance'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'betaWalkTravelCost'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'betaWalkTravelCostPower2'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'opportunitiySamplingRate'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'betaWalkLnTravelCost'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'useCarParameterFromMATSim'), pyxb.binding.datatypes.boolean, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'useBikeParameterFromMATSim'), pyxb.binding.datatypes.boolean, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'useLogitScaleParameterFromMATSim'), pyxb.binding.datatypes.boolean, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'useWalkParameterFromMATSim'), pyxb.binding.datatypes.boolean, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'useRawSumsWithoutLn'), pyxb.binding.datatypes.boolean, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'betaBikeLnTravelDistance'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'logitScaleParameter'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'betaCarTravelTime'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'betaCarTravelTimePower2'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'betaCarLnTravelTime'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'betaCarTravelDistance'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'betaCarTravelDistancePower2'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))

accessibilityParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'betaCarLnTravelDistance'), pyxb.binding.datatypes.double, scope=accessibilityParameterType))
accessibilityParameterType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'opportunitiySamplingRate')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'useLogitScaleParameterFromMATSim')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'useCarParameterFromMATSim')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'useBikeParameterFromMATSim')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'useWalkParameterFromMATSim')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'useRawSumsWithoutLn')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'logitScaleParameter')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'betaCarTravelTime')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'betaCarTravelTimePower2')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'betaCarLnTravelTime')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'betaCarTravelDistance')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'betaCarTravelDistancePower2')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'betaCarLnTravelDistance')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'betaCarTravelCost')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'betaCarTravelCostPower2')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'betaCarLnTravelCost')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'betaBikeTravelTime')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'betaBikeTravelTimePower2')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'betaBikeLnTravelTime')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'betaBikeTravelDistance')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'betaBikeTravelDistancePower2')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'betaBikeLnTravelDistance')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'betaBikeTravelCost')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'betaBikeTravelCostPower2')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'betaBikeLnTravelCost')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'betaWalkTravelTime')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'betaWalkTravelTimePower2')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'betaWalkLnTravelTime')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'betaWalkTravelDistance')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'betaWalkTravelDistancePower2')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'betaWalkLnTravelDistance')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'betaWalkTravelCost')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'betaWalkTravelCostPower2')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(accessibilityParameterType._UseForTag(pyxb.namespace.ExpandedName(None, 'betaWalkLnTravelCost')), min_occurs=1, max_occurs=1)
    )
accessibilityParameterType._ContentModel = pyxb.binding.content.ParticleModel(accessibilityParameterType._GroupModel, min_occurs=1, max_occurs=1)



planCalcScoreType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'homeActivityTypicalDuration'), pyxb.binding.datatypes.nonNegativeInteger, scope=planCalcScoreType))

planCalcScoreType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'workActivityTypicalDuration'), pyxb.binding.datatypes.nonNegativeInteger, scope=planCalcScoreType))

planCalcScoreType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'workActivityOpeningTime'), pyxb.binding.datatypes.nonNegativeInteger, scope=planCalcScoreType))

planCalcScoreType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'activityType_1'), pyxb.binding.datatypes.token, scope=planCalcScoreType))

planCalcScoreType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'workActivityLatestStartTime'), pyxb.binding.datatypes.nonNegativeInteger, scope=planCalcScoreType))

planCalcScoreType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'activityType_0'), pyxb.binding.datatypes.token, scope=planCalcScoreType))
planCalcScoreType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(planCalcScoreType._UseForTag(pyxb.namespace.ExpandedName(None, 'activityType_0')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(planCalcScoreType._UseForTag(pyxb.namespace.ExpandedName(None, 'activityType_1')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(planCalcScoreType._UseForTag(pyxb.namespace.ExpandedName(None, 'homeActivityTypicalDuration')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(planCalcScoreType._UseForTag(pyxb.namespace.ExpandedName(None, 'workActivityTypicalDuration')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(planCalcScoreType._UseForTag(pyxb.namespace.ExpandedName(None, 'workActivityOpeningTime')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(planCalcScoreType._UseForTag(pyxb.namespace.ExpandedName(None, 'workActivityLatestStartTime')), min_occurs=1, max_occurs=1)
    )
planCalcScoreType._ContentModel = pyxb.binding.content.ParticleModel(planCalcScoreType._GroupModel, min_occurs=1, max_occurs=1)



matsim4urbansimContolerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'cellSizeCellBasedAccessibility'), pyxb.binding.datatypes.nonNegativeInteger, scope=matsim4urbansimContolerType))

matsim4urbansimContolerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'cellBasedAccessibility'), pyxb.binding.datatypes.boolean, scope=matsim4urbansimContolerType))

matsim4urbansimContolerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'agentPerformance'), pyxb.binding.datatypes.boolean, scope=matsim4urbansimContolerType))

matsim4urbansimContolerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'shapeFileCellBasedAccessibility'), fileType, scope=matsim4urbansimContolerType))

matsim4urbansimContolerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'useCustomBoundingBox'), pyxb.binding.datatypes.boolean, scope=matsim4urbansimContolerType))

matsim4urbansimContolerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'timeOfADay'), pyxb.binding.datatypes.double, scope=matsim4urbansimContolerType))

matsim4urbansimContolerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'boundingBoxTop'), pyxb.binding.datatypes.double, scope=matsim4urbansimContolerType))

matsim4urbansimContolerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'boundingBoxLeft'), pyxb.binding.datatypes.double, scope=matsim4urbansimContolerType))

matsim4urbansimContolerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'zone2zoneImpedance'), pyxb.binding.datatypes.boolean, scope=matsim4urbansimContolerType))

matsim4urbansimContolerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'boundingBoxRight'), pyxb.binding.datatypes.double, scope=matsim4urbansimContolerType))

matsim4urbansimContolerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'boundingBoxBottom'), pyxb.binding.datatypes.double, scope=matsim4urbansimContolerType))

matsim4urbansimContolerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'zoneBasedAccessibility'), pyxb.binding.datatypes.boolean, scope=matsim4urbansimContolerType))
matsim4urbansimContolerType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(matsim4urbansimContolerType._UseForTag(pyxb.namespace.ExpandedName(None, 'zone2zoneImpedance')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimContolerType._UseForTag(pyxb.namespace.ExpandedName(None, 'agentPerformance')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimContolerType._UseForTag(pyxb.namespace.ExpandedName(None, 'zoneBasedAccessibility')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimContolerType._UseForTag(pyxb.namespace.ExpandedName(None, 'cellBasedAccessibility')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimContolerType._UseForTag(pyxb.namespace.ExpandedName(None, 'cellSizeCellBasedAccessibility')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimContolerType._UseForTag(pyxb.namespace.ExpandedName(None, 'shapeFileCellBasedAccessibility')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimContolerType._UseForTag(pyxb.namespace.ExpandedName(None, 'useCustomBoundingBox')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimContolerType._UseForTag(pyxb.namespace.ExpandedName(None, 'boundingBoxTop')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimContolerType._UseForTag(pyxb.namespace.ExpandedName(None, 'boundingBoxLeft')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimContolerType._UseForTag(pyxb.namespace.ExpandedName(None, 'boundingBoxRight')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimContolerType._UseForTag(pyxb.namespace.ExpandedName(None, 'boundingBoxBottom')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimContolerType._UseForTag(pyxb.namespace.ExpandedName(None, 'timeOfADay')), min_occurs=1, max_occurs=1)
    )
matsim4urbansimContolerType._ContentModel = pyxb.binding.content.ParticleModel(matsim4urbansimContolerType._GroupModel, min_occurs=1, max_occurs=1)



configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'inputPlansFile'), inputPlansFileType, scope=configType))

configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'controler'), controlerType, scope=configType))

configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'planCalcScore'), planCalcScoreType, scope=configType))

configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'hotStartPlansFile'), inputPlansFileType, scope=configType))

configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'strategy'), strategyType, scope=configType))

configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'matsim_config'), fileType, scope=configType))

configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'network'), fileType, scope=configType))
configType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(configType._UseForTag(pyxb.namespace.ExpandedName(None, 'matsim_config')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(configType._UseForTag(pyxb.namespace.ExpandedName(None, 'network')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(configType._UseForTag(pyxb.namespace.ExpandedName(None, 'inputPlansFile')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(configType._UseForTag(pyxb.namespace.ExpandedName(None, 'hotStartPlansFile')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(configType._UseForTag(pyxb.namespace.ExpandedName(None, 'controler')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(configType._UseForTag(pyxb.namespace.ExpandedName(None, 'planCalcScore')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(configType._UseForTag(pyxb.namespace.ExpandedName(None, 'strategy')), min_occurs=1, max_occurs=1)
    )
configType._ContentModel = pyxb.binding.content.ParticleModel(configType._GroupModel, min_occurs=1, max_occurs=1)



matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'accessibilityParameter'), accessibilityParameterType, scope=matsim4urbansimType))

matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'urbansimParameter'), urbansimParameterType, scope=matsim4urbansimType))

matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'matsim4urbansimContoler'), matsim4urbansimContolerType, scope=matsim4urbansimType))
matsim4urbansimType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, 'urbansimParameter')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, 'matsim4urbansimContoler')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, 'accessibilityParameter')), min_occurs=1, max_occurs=1)
    )
matsim4urbansimType._ContentModel = pyxb.binding.content.ParticleModel(matsim4urbansimType._GroupModel, min_occurs=1, max_occurs=1)
