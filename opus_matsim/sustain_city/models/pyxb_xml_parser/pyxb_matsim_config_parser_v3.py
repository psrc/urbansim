# Opus/UrbanSim urban simulation software
# Copyright (C) 2010-2012 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

# ./pyxb_matsim_config_parser_v3.py
# PyXB bindings for NM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2013-06-18 12:28:16.201263 by PyXB version 1.1.3
# Namespace AbsentNamespace0

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:c97c1385-d801-11e2-851c-3c07544cd942')

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


# Complex type matsim_configType with content type ELEMENT_ONLY
class matsim_configType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'matsim_configType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element network uses Python identifier network
    __network = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'network'), 'network', '__AbsentNamespace0_matsim_configType_network', False)

    
    network = property(__network.value, __network.set, None, None)

    
    # Element warmStartPlansFile uses Python identifier warmStartPlansFile
    __warmStartPlansFile = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'warmStartPlansFile'), 'warmStartPlansFile', '__AbsentNamespace0_matsim_configType_warmStartPlansFile', False)

    
    warmStartPlansFile = property(__warmStartPlansFile.value, __warmStartPlansFile.set, None, None)

    
    # Element useHotStart uses Python identifier useHotStart
    __useHotStart = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'useHotStart'), 'useHotStart', '__AbsentNamespace0_matsim_configType_useHotStart', False)

    
    useHotStart = property(__useHotStart.value, __useHotStart.set, None, None)

    
    # Element hotStartPlansFile uses Python identifier hotStartPlansFile
    __hotStartPlansFile = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'hotStartPlansFile'), 'hotStartPlansFile', '__AbsentNamespace0_matsim_configType_hotStartPlansFile', False)

    
    hotStartPlansFile = property(__hotStartPlansFile.value, __hotStartPlansFile.set, None, None)

    
    # Element activityType_0 uses Python identifier activityType_0
    __activityType_0 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'activityType_0'), 'activityType_0', '__AbsentNamespace0_matsim_configType_activityType_0', False)

    
    activityType_0 = property(__activityType_0.value, __activityType_0.set, None, None)

    
    # Element activityType_1 uses Python identifier activityType_1
    __activityType_1 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'activityType_1'), 'activityType_1', '__AbsentNamespace0_matsim_configType_activityType_1', False)

    
    activityType_1 = property(__activityType_1.value, __activityType_1.set, None, None)

    
    # Element homeActivityTypicalDuration uses Python identifier homeActivityTypicalDuration
    __homeActivityTypicalDuration = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'homeActivityTypicalDuration'), 'homeActivityTypicalDuration', '__AbsentNamespace0_matsim_configType_homeActivityTypicalDuration', False)

    
    homeActivityTypicalDuration = property(__homeActivityTypicalDuration.value, __homeActivityTypicalDuration.set, None, None)

    
    # Element workActivityTypicalDuration uses Python identifier workActivityTypicalDuration
    __workActivityTypicalDuration = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'workActivityTypicalDuration'), 'workActivityTypicalDuration', '__AbsentNamespace0_matsim_configType_workActivityTypicalDuration', False)

    
    workActivityTypicalDuration = property(__workActivityTypicalDuration.value, __workActivityTypicalDuration.set, None, None)

    
    # Element workActivityLatestStartTime uses Python identifier workActivityLatestStartTime
    __workActivityLatestStartTime = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'workActivityLatestStartTime'), 'workActivityLatestStartTime', '__AbsentNamespace0_matsim_configType_workActivityLatestStartTime', False)

    
    workActivityLatestStartTime = property(__workActivityLatestStartTime.value, __workActivityLatestStartTime.set, None, None)

    
    # Element firstIteration uses Python identifier firstIteration
    __firstIteration = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'firstIteration'), 'firstIteration', '__AbsentNamespace0_matsim_configType_firstIteration', False)

    
    firstIteration = property(__firstIteration.value, __firstIteration.set, None, None)

    
    # Element lastIteration uses Python identifier lastIteration
    __lastIteration = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'lastIteration'), 'lastIteration', '__AbsentNamespace0_matsim_configType_lastIteration', False)

    
    lastIteration = property(__lastIteration.value, __lastIteration.set, None, None)

    
    # Element cellSize uses Python identifier cellSize
    __cellSize = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'cellSize'), 'cellSize', '__AbsentNamespace0_matsim_configType_cellSize', False)

    
    cellSize = property(__cellSize.value, __cellSize.set, None, None)

    
    # Element studyAreaBoundaryShapeFile uses Python identifier studyAreaBoundaryShapeFile
    __studyAreaBoundaryShapeFile = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'studyAreaBoundaryShapeFile'), 'studyAreaBoundaryShapeFile', '__AbsentNamespace0_matsim_configType_studyAreaBoundaryShapeFile', False)

    
    studyAreaBoundaryShapeFile = property(__studyAreaBoundaryShapeFile.value, __studyAreaBoundaryShapeFile.set, None, None)

    
    # Element accessibilityComputationAreaFromShapeFile uses Python identifier accessibilityComputationAreaFromShapeFile
    __accessibilityComputationAreaFromShapeFile = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'accessibilityComputationAreaFromShapeFile'), 'accessibilityComputationAreaFromShapeFile', '__AbsentNamespace0_matsim_configType_accessibilityComputationAreaFromShapeFile', False)

    
    accessibilityComputationAreaFromShapeFile = property(__accessibilityComputationAreaFromShapeFile.value, __accessibilityComputationAreaFromShapeFile.set, None, None)

    
    # Element accessibilityComputationAreaFromBoundingBox uses Python identifier accessibilityComputationAreaFromBoundingBox
    __accessibilityComputationAreaFromBoundingBox = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'accessibilityComputationAreaFromBoundingBox'), 'accessibilityComputationAreaFromBoundingBox', '__AbsentNamespace0_matsim_configType_accessibilityComputationAreaFromBoundingBox', False)

    
    accessibilityComputationAreaFromBoundingBox = property(__accessibilityComputationAreaFromBoundingBox.value, __accessibilityComputationAreaFromBoundingBox.set, None, None)

    
    # Element accessibilityComputationAreaFromNetwork uses Python identifier accessibilityComputationAreaFromNetwork
    __accessibilityComputationAreaFromNetwork = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'accessibilityComputationAreaFromNetwork'), 'accessibilityComputationAreaFromNetwork', '__AbsentNamespace0_matsim_configType_accessibilityComputationAreaFromNetwork', False)

    
    accessibilityComputationAreaFromNetwork = property(__accessibilityComputationAreaFromNetwork.value, __accessibilityComputationAreaFromNetwork.set, None, None)

    
    # Element workActivityOpeningTime uses Python identifier workActivityOpeningTime
    __workActivityOpeningTime = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'workActivityOpeningTime'), 'workActivityOpeningTime', '__AbsentNamespace0_matsim_configType_workActivityOpeningTime', False)

    
    workActivityOpeningTime = property(__workActivityOpeningTime.value, __workActivityOpeningTime.set, None, None)

    
    # Element boundingBoxTop uses Python identifier boundingBoxTop
    __boundingBoxTop = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'boundingBoxTop'), 'boundingBoxTop', '__AbsentNamespace0_matsim_configType_boundingBoxTop', False)

    
    boundingBoxTop = property(__boundingBoxTop.value, __boundingBoxTop.set, None, None)

    
    # Element boundingBoxLeft uses Python identifier boundingBoxLeft
    __boundingBoxLeft = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'boundingBoxLeft'), 'boundingBoxLeft', '__AbsentNamespace0_matsim_configType_boundingBoxLeft', False)

    
    boundingBoxLeft = property(__boundingBoxLeft.value, __boundingBoxLeft.set, None, None)

    
    # Element boundingBoxRight uses Python identifier boundingBoxRight
    __boundingBoxRight = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'boundingBoxRight'), 'boundingBoxRight', '__AbsentNamespace0_matsim_configType_boundingBoxRight', False)

    
    boundingBoxRight = property(__boundingBoxRight.value, __boundingBoxRight.set, None, None)

    
    # Element boundingBoxBottom uses Python identifier boundingBoxBottom
    __boundingBoxBottom = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'boundingBoxBottom'), 'boundingBoxBottom', '__AbsentNamespace0_matsim_configType_boundingBoxBottom', False)

    
    boundingBoxBottom = property(__boundingBoxBottom.value, __boundingBoxBottom.set, None, None)

    
    # Element urbansimZoneRandomLocationDistributionByRadius uses Python identifier urbansimZoneRandomLocationDistributionByRadius
    __urbansimZoneRandomLocationDistributionByRadius = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'urbansimZoneRandomLocationDistributionByRadius'), 'urbansimZoneRandomLocationDistributionByRadius', '__AbsentNamespace0_matsim_configType_urbansimZoneRandomLocationDistributionByRadius', False)

    
    urbansimZoneRandomLocationDistributionByRadius = property(__urbansimZoneRandomLocationDistributionByRadius.value, __urbansimZoneRandomLocationDistributionByRadius.set, None, None)

    
    # Element urbansimZoneRandomLocationDistributionByShapeFile uses Python identifier urbansimZoneRandomLocationDistributionByShapeFile
    __urbansimZoneRandomLocationDistributionByShapeFile = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'urbansimZoneRandomLocationDistributionByShapeFile'), 'urbansimZoneRandomLocationDistributionByShapeFile', '__AbsentNamespace0_matsim_configType_urbansimZoneRandomLocationDistributionByShapeFile', False)

    
    urbansimZoneRandomLocationDistributionByShapeFile = property(__urbansimZoneRandomLocationDistributionByShapeFile.value, __urbansimZoneRandomLocationDistributionByShapeFile.set, None, None)

    
    # Element external_matsim_config uses Python identifier external_matsim_config
    __external_matsim_config = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'external_matsim_config'), 'external_matsim_config', '__AbsentNamespace0_matsim_configType_external_matsim_config', False)

    
    external_matsim_config = property(__external_matsim_config.value, __external_matsim_config.set, None, None)


    _ElementMap = {
        __network.name() : __network,
        __warmStartPlansFile.name() : __warmStartPlansFile,
        __useHotStart.name() : __useHotStart,
        __hotStartPlansFile.name() : __hotStartPlansFile,
        __activityType_0.name() : __activityType_0,
        __activityType_1.name() : __activityType_1,
        __homeActivityTypicalDuration.name() : __homeActivityTypicalDuration,
        __workActivityTypicalDuration.name() : __workActivityTypicalDuration,
        __workActivityLatestStartTime.name() : __workActivityLatestStartTime,
        __firstIteration.name() : __firstIteration,
        __lastIteration.name() : __lastIteration,
        __cellSize.name() : __cellSize,
        __studyAreaBoundaryShapeFile.name() : __studyAreaBoundaryShapeFile,
        __accessibilityComputationAreaFromShapeFile.name() : __accessibilityComputationAreaFromShapeFile,
        __accessibilityComputationAreaFromBoundingBox.name() : __accessibilityComputationAreaFromBoundingBox,
        __accessibilityComputationAreaFromNetwork.name() : __accessibilityComputationAreaFromNetwork,
        __workActivityOpeningTime.name() : __workActivityOpeningTime,
        __boundingBoxTop.name() : __boundingBoxTop,
        __boundingBoxLeft.name() : __boundingBoxLeft,
        __boundingBoxRight.name() : __boundingBoxRight,
        __boundingBoxBottom.name() : __boundingBoxBottom,
        __urbansimZoneRandomLocationDistributionByRadius.name() : __urbansimZoneRandomLocationDistributionByRadius,
        __urbansimZoneRandomLocationDistributionByShapeFile.name() : __urbansimZoneRandomLocationDistributionByShapeFile,
        __external_matsim_config.name() : __external_matsim_config
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'matsim_configType', matsim_configType)


# Complex type matsim4urbansimType with content type ELEMENT_ONLY
class matsim4urbansimType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'matsim4urbansimType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element matsim4opus uses Python identifier matsim4opus
    __matsim4opus = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'matsim4opus'), 'matsim4opus', '__AbsentNamespace0_matsim4urbansimType_matsim4opus', False)

    
    matsim4opus = property(__matsim4opus.value, __matsim4opus.set, None, None)

    
    # Element opusDataPath uses Python identifier opusDataPath
    __opusDataPath = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'opusDataPath'), 'opusDataPath', '__AbsentNamespace0_matsim4urbansimType_opusDataPath', False)

    
    opusDataPath = property(__opusDataPath.value, __opusDataPath.set, None, None)

    
    # Element matsim4opusConfig uses Python identifier matsim4opusConfig
    __matsim4opusConfig = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'matsim4opusConfig'), 'matsim4opusConfig', '__AbsentNamespace0_matsim4urbansimType_matsim4opusConfig', False)

    
    matsim4opusConfig = property(__matsim4opusConfig.value, __matsim4opusConfig.set, None, None)

    
    # Element backupRunData uses Python identifier backupRunData
    __backupRunData = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'backupRunData'), 'backupRunData', '__AbsentNamespace0_matsim4urbansimType_backupRunData', False)

    
    backupRunData = property(__backupRunData.value, __backupRunData.set, None, None)

    
    # Element agentPerfomance uses Python identifier agentPerfomance
    __agentPerfomance = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'agentPerfomance'), 'agentPerfomance', '__AbsentNamespace0_matsim4urbansimType_agentPerfomance', False)

    
    agentPerfomance = property(__agentPerfomance.value, __agentPerfomance.set, None, None)

    
    # Element matsim4opusOutput uses Python identifier matsim4opusOutput
    __matsim4opusOutput = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'matsim4opusOutput'), 'matsim4opusOutput', '__AbsentNamespace0_matsim4urbansimType_matsim4opusOutput', False)

    
    matsim4opusOutput = property(__matsim4opusOutput.value, __matsim4opusOutput.set, None, None)

    
    # Element matsim4opusTemp uses Python identifier matsim4opusTemp
    __matsim4opusTemp = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'matsim4opusTemp'), 'matsim4opusTemp', '__AbsentNamespace0_matsim4urbansimType_matsim4opusTemp', False)

    
    matsim4opusTemp = property(__matsim4opusTemp.value, __matsim4opusTemp.set, None, None)

    
    # Element parcelBasedAccessibility uses Python identifier parcelBasedAccessibility
    __parcelBasedAccessibility = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'parcelBasedAccessibility'), 'parcelBasedAccessibility', '__AbsentNamespace0_matsim4urbansimType_parcelBasedAccessibility', False)

    
    parcelBasedAccessibility = property(__parcelBasedAccessibility.value, __parcelBasedAccessibility.set, None, None)

    
    # Element populationSamplingRate uses Python identifier populationSamplingRate
    __populationSamplingRate = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'populationSamplingRate'), 'populationSamplingRate', '__AbsentNamespace0_matsim4urbansimType_populationSamplingRate', False)

    
    populationSamplingRate = property(__populationSamplingRate.value, __populationSamplingRate.set, None, None)

    
    # Element year uses Python identifier year
    __year = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'year'), 'year', '__AbsentNamespace0_matsim4urbansimType_year', False)

    
    year = property(__year.value, __year.set, None, None)

    
    # Element zone2ZoneImpedance uses Python identifier zone2ZoneImpedance
    __zone2ZoneImpedance = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'zone2ZoneImpedance'), 'zone2ZoneImpedance', '__AbsentNamespace0_matsim4urbansimType_zone2ZoneImpedance', False)

    
    zone2ZoneImpedance = property(__zone2ZoneImpedance.value, __zone2ZoneImpedance.set, None, None)

    
    # Element opusHome uses Python identifier opusHome
    __opusHome = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'opusHome'), 'opusHome', '__AbsentNamespace0_matsim4urbansimType_opusHome', False)

    
    opusHome = property(__opusHome.value, __opusHome.set, None, None)

    
    # Element customParameter uses Python identifier customParameter
    __customParameter = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'customParameter'), 'customParameter', '__AbsentNamespace0_matsim4urbansimType_customParameter', False)

    
    customParameter = property(__customParameter.value, __customParameter.set, None, None)

    
    # Element zoneBasedAccessibility uses Python identifier zoneBasedAccessibility
    __zoneBasedAccessibility = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'zoneBasedAccessibility'), 'zoneBasedAccessibility', '__AbsentNamespace0_matsim4urbansimType_zoneBasedAccessibility', False)

    
    zoneBasedAccessibility = property(__zoneBasedAccessibility.value, __zoneBasedAccessibility.set, None, None)


    _ElementMap = {
        __matsim4opus.name() : __matsim4opus,
        __opusDataPath.name() : __opusDataPath,
        __matsim4opusConfig.name() : __matsim4opusConfig,
        __backupRunData.name() : __backupRunData,
        __agentPerfomance.name() : __agentPerfomance,
        __matsim4opusOutput.name() : __matsim4opusOutput,
        __matsim4opusTemp.name() : __matsim4opusTemp,
        __parcelBasedAccessibility.name() : __parcelBasedAccessibility,
        __populationSamplingRate.name() : __populationSamplingRate,
        __year.name() : __year,
        __zone2ZoneImpedance.name() : __zone2ZoneImpedance,
        __opusHome.name() : __opusHome,
        __customParameter.name() : __customParameter,
        __zoneBasedAccessibility.name() : __zoneBasedAccessibility
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'matsim4urbansimType', matsim4urbansimType)


# Complex type matsim4urbansim_configType with content type ELEMENT_ONLY
class matsim4urbansim_configType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'matsim4urbansim_configType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element matsim4urbansim uses Python identifier matsim4urbansim
    __matsim4urbansim = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'matsim4urbansim'), 'matsim4urbansim', '__AbsentNamespace0_matsim4urbansim_configType_matsim4urbansim', False)

    
    matsim4urbansim = property(__matsim4urbansim.value, __matsim4urbansim.set, None, None)

    
    # Element matsim_config uses Python identifier matsim_config
    __matsim_config = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'matsim_config'), 'matsim_config', '__AbsentNamespace0_matsim4urbansim_configType_matsim_config', False)

    
    matsim_config = property(__matsim_config.value, __matsim_config.set, None, None)


    _ElementMap = {
        __matsim4urbansim.name() : __matsim4urbansim,
        __matsim_config.name() : __matsim_config
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'matsim4urbansim_configType', matsim4urbansim_configType)


matsim4urbansim_config = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'matsim4urbansim_config'), matsim4urbansim_configType)
Namespace.addCategoryObject('elementBinding', matsim4urbansim_config.name().localName(), matsim4urbansim_config)



matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'network'), pyxb.binding.datatypes.token, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'warmStartPlansFile'), pyxb.binding.datatypes.token, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'useHotStart'), pyxb.binding.datatypes.boolean, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'hotStartPlansFile'), pyxb.binding.datatypes.token, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'activityType_0'), pyxb.binding.datatypes.token, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'activityType_1'), pyxb.binding.datatypes.token, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'homeActivityTypicalDuration'), pyxb.binding.datatypes.nonNegativeInteger, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'workActivityTypicalDuration'), pyxb.binding.datatypes.nonNegativeInteger, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'workActivityLatestStartTime'), pyxb.binding.datatypes.nonNegativeInteger, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'firstIteration'), pyxb.binding.datatypes.nonNegativeInteger, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'lastIteration'), pyxb.binding.datatypes.nonNegativeInteger, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'cellSize'), pyxb.binding.datatypes.nonNegativeInteger, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'studyAreaBoundaryShapeFile'), pyxb.binding.datatypes.token, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'accessibilityComputationAreaFromShapeFile'), pyxb.binding.datatypes.boolean, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'accessibilityComputationAreaFromBoundingBox'), pyxb.binding.datatypes.boolean, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'accessibilityComputationAreaFromNetwork'), pyxb.binding.datatypes.boolean, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'workActivityOpeningTime'), pyxb.binding.datatypes.nonNegativeInteger, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'boundingBoxTop'), pyxb.binding.datatypes.double, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'boundingBoxLeft'), pyxb.binding.datatypes.double, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'boundingBoxRight'), pyxb.binding.datatypes.double, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'boundingBoxBottom'), pyxb.binding.datatypes.double, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'urbansimZoneRandomLocationDistributionByRadius'), pyxb.binding.datatypes.double, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'urbansimZoneRandomLocationDistributionByShapeFile'), pyxb.binding.datatypes.token, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'external_matsim_config'), pyxb.binding.datatypes.token, scope=matsim_configType))
matsim_configType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, u'cellSize')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, u'accessibilityComputationAreaFromShapeFile')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, u'accessibilityComputationAreaFromBoundingBox')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, u'accessibilityComputationAreaFromNetwork')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, u'studyAreaBoundaryShapeFile')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, u'boundingBoxTop')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, u'boundingBoxLeft')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, u'boundingBoxRight')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, u'boundingBoxBottom')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, u'urbansimZoneRandomLocationDistributionByRadius')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, u'urbansimZoneRandomLocationDistributionByShapeFile')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, u'external_matsim_config')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, u'network')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, u'warmStartPlansFile')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, u'useHotStart')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, u'hotStartPlansFile')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, u'activityType_0')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, u'activityType_1')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, u'homeActivityTypicalDuration')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, u'workActivityTypicalDuration')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, u'workActivityOpeningTime')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, u'workActivityLatestStartTime')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, u'firstIteration')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, u'lastIteration')), min_occurs=1, max_occurs=1)
    )
matsim_configType._ContentModel = pyxb.binding.content.ParticleModel(matsim_configType._GroupModel, min_occurs=1, max_occurs=1)



matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'matsim4opus'), pyxb.binding.datatypes.token, scope=matsim4urbansimType))

matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'opusDataPath'), pyxb.binding.datatypes.token, scope=matsim4urbansimType))

matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'matsim4opusConfig'), pyxb.binding.datatypes.token, scope=matsim4urbansimType))

matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'backupRunData'), pyxb.binding.datatypes.boolean, scope=matsim4urbansimType))

matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'agentPerfomance'), pyxb.binding.datatypes.boolean, scope=matsim4urbansimType))

matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'matsim4opusOutput'), pyxb.binding.datatypes.token, scope=matsim4urbansimType))

matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'matsim4opusTemp'), pyxb.binding.datatypes.token, scope=matsim4urbansimType))

matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'parcelBasedAccessibility'), pyxb.binding.datatypes.boolean, scope=matsim4urbansimType))

matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'populationSamplingRate'), pyxb.binding.datatypes.double, scope=matsim4urbansimType))

matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'year'), pyxb.binding.datatypes.nonNegativeInteger, scope=matsim4urbansimType))

matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'zone2ZoneImpedance'), pyxb.binding.datatypes.boolean, scope=matsim4urbansimType))

matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'opusHome'), pyxb.binding.datatypes.token, scope=matsim4urbansimType))

matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'customParameter'), pyxb.binding.datatypes.token, scope=matsim4urbansimType))

matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'zoneBasedAccessibility'), pyxb.binding.datatypes.boolean, scope=matsim4urbansimType))
matsim4urbansimType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, u'populationSamplingRate')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, u'year')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, u'opusHome')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, u'opusDataPath')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, u'matsim4opus')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, u'matsim4opusConfig')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, u'matsim4opusOutput')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, u'matsim4opusTemp')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, u'customParameter')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, u'zone2ZoneImpedance')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, u'agentPerfomance')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, u'zoneBasedAccessibility')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, u'parcelBasedAccessibility')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, u'backupRunData')), min_occurs=1, max_occurs=1)
    )
matsim4urbansimType._ContentModel = pyxb.binding.content.ParticleModel(matsim4urbansimType._GroupModel, min_occurs=1, max_occurs=1)



matsim4urbansim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'matsim4urbansim'), matsim4urbansimType, scope=matsim4urbansim_configType))

matsim4urbansim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'matsim_config'), matsim_configType, scope=matsim4urbansim_configType))
matsim4urbansim_configType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(matsim4urbansim_configType._UseForTag(pyxb.namespace.ExpandedName(None, u'matsim_config')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(matsim4urbansim_configType._UseForTag(pyxb.namespace.ExpandedName(None, u'matsim4urbansim')), min_occurs=1L, max_occurs=1L)
    )
matsim4urbansim_configType._ContentModel = pyxb.binding.content.ParticleModel(matsim4urbansim_configType._GroupModel, min_occurs=1, max_occurs=1)
