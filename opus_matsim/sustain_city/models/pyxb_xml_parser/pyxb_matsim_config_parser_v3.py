# Opus/UrbanSim urban simulation software
# Copyright (C) 2010-2012 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

# ./pyxb_matsim_config_parser_v3.py
# PyXB bindings for NM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2013-06-25 10:49:05.675783 by PyXB version 1.1.3
# Namespace AbsentNamespace0

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:1780d457-dd74-11e2-997e-3c07544cd942')

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


# Complex type matsim_configType with content type ELEMENT_ONLY
class matsim_configType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'matsim_configType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element studyAreaBoundaryShapeFile uses Python identifier studyAreaBoundaryShapeFile
    __studyAreaBoundaryShapeFile = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'studyAreaBoundaryShapeFile'), 'studyAreaBoundaryShapeFile', '__AbsentNamespace0_matsim_configType_studyAreaBoundaryShapeFile', False)

    
    studyAreaBoundaryShapeFile = property(__studyAreaBoundaryShapeFile.value, __studyAreaBoundaryShapeFile.set, None, None)

    
    # Element boundingBoxLeft uses Python identifier boundingBoxLeft
    __boundingBoxLeft = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'boundingBoxLeft'), 'boundingBoxLeft', '__AbsentNamespace0_matsim_configType_boundingBoxLeft', False)

    
    boundingBoxLeft = property(__boundingBoxLeft.value, __boundingBoxLeft.set, None, None)

    
    # Element boundingBoxRight uses Python identifier boundingBoxRight
    __boundingBoxRight = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'boundingBoxRight'), 'boundingBoxRight', '__AbsentNamespace0_matsim_configType_boundingBoxRight', False)

    
    boundingBoxRight = property(__boundingBoxRight.value, __boundingBoxRight.set, None, None)

    
    # Element boundingBoxTop uses Python identifier boundingBoxTop
    __boundingBoxTop = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'boundingBoxTop'), 'boundingBoxTop', '__AbsentNamespace0_matsim_configType_boundingBoxTop', False)

    
    boundingBoxTop = property(__boundingBoxTop.value, __boundingBoxTop.set, None, None)

    
    # Element boundingBoxBottom uses Python identifier boundingBoxBottom
    __boundingBoxBottom = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'boundingBoxBottom'), 'boundingBoxBottom', '__AbsentNamespace0_matsim_configType_boundingBoxBottom', False)

    
    boundingBoxBottom = property(__boundingBoxBottom.value, __boundingBoxBottom.set, None, None)

    
    # Element urbansimZoneRandomLocationDistributionByRadius uses Python identifier urbansimZoneRandomLocationDistributionByRadius
    __urbansimZoneRandomLocationDistributionByRadius = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'urbansimZoneRandomLocationDistributionByRadius'), 'urbansimZoneRandomLocationDistributionByRadius', '__AbsentNamespace0_matsim_configType_urbansimZoneRandomLocationDistributionByRadius', False)

    
    urbansimZoneRandomLocationDistributionByRadius = property(__urbansimZoneRandomLocationDistributionByRadius.value, __urbansimZoneRandomLocationDistributionByRadius.set, None, None)

    
    # Element urbansimZoneRandomLocationDistributionByShapeFile uses Python identifier urbansimZoneRandomLocationDistributionByShapeFile
    __urbansimZoneRandomLocationDistributionByShapeFile = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'urbansimZoneRandomLocationDistributionByShapeFile'), 'urbansimZoneRandomLocationDistributionByShapeFile', '__AbsentNamespace0_matsim_configType_urbansimZoneRandomLocationDistributionByShapeFile', False)

    
    urbansimZoneRandomLocationDistributionByShapeFile = property(__urbansimZoneRandomLocationDistributionByShapeFile.value, __urbansimZoneRandomLocationDistributionByShapeFile.set, None, None)

    
    # Element external_matsim_config uses Python identifier external_matsim_config
    __external_matsim_config = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'external_matsim_config'), 'external_matsim_config', '__AbsentNamespace0_matsim_configType_external_matsim_config', False)

    
    external_matsim_config = property(__external_matsim_config.value, __external_matsim_config.set, None, None)

    
    # Element warmStartPlansFile uses Python identifier warmStartPlansFile
    __warmStartPlansFile = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'warmStartPlansFile'), 'warmStartPlansFile', '__AbsentNamespace0_matsim_configType_warmStartPlansFile', False)

    
    warmStartPlansFile = property(__warmStartPlansFile.value, __warmStartPlansFile.set, None, None)

    
    # Element useHotStart uses Python identifier useHotStart
    __useHotStart = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'useHotStart'), 'useHotStart', '__AbsentNamespace0_matsim_configType_useHotStart', False)

    
    useHotStart = property(__useHotStart.value, __useHotStart.set, None, None)

    
    # Element hotStartPlansFile uses Python identifier hotStartPlansFile
    __hotStartPlansFile = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'hotStartPlansFile'), 'hotStartPlansFile', '__AbsentNamespace0_matsim_configType_hotStartPlansFile', False)

    
    hotStartPlansFile = property(__hotStartPlansFile.value, __hotStartPlansFile.set, None, None)

    
    # Element activityType_0 uses Python identifier activityType_0
    __activityType_0 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'activityType_0'), 'activityType_0', '__AbsentNamespace0_matsim_configType_activityType_0', False)

    
    activityType_0 = property(__activityType_0.value, __activityType_0.set, None, None)

    
    # Element activityType_1 uses Python identifier activityType_1
    __activityType_1 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'activityType_1'), 'activityType_1', '__AbsentNamespace0_matsim_configType_activityType_1', False)

    
    activityType_1 = property(__activityType_1.value, __activityType_1.set, None, None)

    
    # Element homeActivityTypicalDuration uses Python identifier homeActivityTypicalDuration
    __homeActivityTypicalDuration = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'homeActivityTypicalDuration'), 'homeActivityTypicalDuration', '__AbsentNamespace0_matsim_configType_homeActivityTypicalDuration', False)

    
    homeActivityTypicalDuration = property(__homeActivityTypicalDuration.value, __homeActivityTypicalDuration.set, None, None)

    
    # Element workActivityTypicalDuration uses Python identifier workActivityTypicalDuration
    __workActivityTypicalDuration = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'workActivityTypicalDuration'), 'workActivityTypicalDuration', '__AbsentNamespace0_matsim_configType_workActivityTypicalDuration', False)

    
    workActivityTypicalDuration = property(__workActivityTypicalDuration.value, __workActivityTypicalDuration.set, None, None)

    
    # Element workActivityOpeningTime uses Python identifier workActivityOpeningTime
    __workActivityOpeningTime = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'workActivityOpeningTime'), 'workActivityOpeningTime', '__AbsentNamespace0_matsim_configType_workActivityOpeningTime', False)

    
    workActivityOpeningTime = property(__workActivityOpeningTime.value, __workActivityOpeningTime.set, None, None)

    
    # Element workActivityLatestStartTime uses Python identifier workActivityLatestStartTime
    __workActivityLatestStartTime = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'workActivityLatestStartTime'), 'workActivityLatestStartTime', '__AbsentNamespace0_matsim_configType_workActivityLatestStartTime', False)

    
    workActivityLatestStartTime = property(__workActivityLatestStartTime.value, __workActivityLatestStartTime.set, None, None)

    
    # Element firstIteration uses Python identifier firstIteration
    __firstIteration = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'firstIteration'), 'firstIteration', '__AbsentNamespace0_matsim_configType_firstIteration', False)

    
    firstIteration = property(__firstIteration.value, __firstIteration.set, None, None)

    
    # Element lastIteration uses Python identifier lastIteration
    __lastIteration = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'lastIteration'), 'lastIteration', '__AbsentNamespace0_matsim_configType_lastIteration', False)

    
    lastIteration = property(__lastIteration.value, __lastIteration.set, None, None)

    
    # Element network uses Python identifier network
    __network = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'network'), 'network', '__AbsentNamespace0_matsim_configType_network', False)

    
    network = property(__network.value, __network.set, None, None)

    
    # Element cellSize uses Python identifier cellSize
    __cellSize = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'cellSize'), 'cellSize', '__AbsentNamespace0_matsim_configType_cellSize', False)

    
    cellSize = property(__cellSize.value, __cellSize.set, None, None)

    
    # Element accessibilityComputationAreaFromShapeFile uses Python identifier accessibilityComputationAreaFromShapeFile
    __accessibilityComputationAreaFromShapeFile = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'accessibilityComputationAreaFromShapeFile'), 'accessibilityComputationAreaFromShapeFile', '__AbsentNamespace0_matsim_configType_accessibilityComputationAreaFromShapeFile', False)

    
    accessibilityComputationAreaFromShapeFile = property(__accessibilityComputationAreaFromShapeFile.value, __accessibilityComputationAreaFromShapeFile.set, None, None)

    
    # Element accessibilityComputationAreaFromBoundingBox uses Python identifier accessibilityComputationAreaFromBoundingBox
    __accessibilityComputationAreaFromBoundingBox = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'accessibilityComputationAreaFromBoundingBox'), 'accessibilityComputationAreaFromBoundingBox', '__AbsentNamespace0_matsim_configType_accessibilityComputationAreaFromBoundingBox', False)

    
    accessibilityComputationAreaFromBoundingBox = property(__accessibilityComputationAreaFromBoundingBox.value, __accessibilityComputationAreaFromBoundingBox.set, None, None)

    
    # Element accessibilityComputationAreaFromNetwork uses Python identifier accessibilityComputationAreaFromNetwork
    __accessibilityComputationAreaFromNetwork = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'accessibilityComputationAreaFromNetwork'), 'accessibilityComputationAreaFromNetwork', '__AbsentNamespace0_matsim_configType_accessibilityComputationAreaFromNetwork', False)

    
    accessibilityComputationAreaFromNetwork = property(__accessibilityComputationAreaFromNetwork.value, __accessibilityComputationAreaFromNetwork.set, None, None)


    _ElementMap = {
        __studyAreaBoundaryShapeFile.name() : __studyAreaBoundaryShapeFile,
        __boundingBoxLeft.name() : __boundingBoxLeft,
        __boundingBoxRight.name() : __boundingBoxRight,
        __boundingBoxTop.name() : __boundingBoxTop,
        __boundingBoxBottom.name() : __boundingBoxBottom,
        __urbansimZoneRandomLocationDistributionByRadius.name() : __urbansimZoneRandomLocationDistributionByRadius,
        __urbansimZoneRandomLocationDistributionByShapeFile.name() : __urbansimZoneRandomLocationDistributionByShapeFile,
        __external_matsim_config.name() : __external_matsim_config,
        __warmStartPlansFile.name() : __warmStartPlansFile,
        __useHotStart.name() : __useHotStart,
        __hotStartPlansFile.name() : __hotStartPlansFile,
        __activityType_0.name() : __activityType_0,
        __activityType_1.name() : __activityType_1,
        __homeActivityTypicalDuration.name() : __homeActivityTypicalDuration,
        __workActivityTypicalDuration.name() : __workActivityTypicalDuration,
        __workActivityOpeningTime.name() : __workActivityOpeningTime,
        __workActivityLatestStartTime.name() : __workActivityLatestStartTime,
        __firstIteration.name() : __firstIteration,
        __lastIteration.name() : __lastIteration,
        __network.name() : __network,
        __cellSize.name() : __cellSize,
        __accessibilityComputationAreaFromShapeFile.name() : __accessibilityComputationAreaFromShapeFile,
        __accessibilityComputationAreaFromBoundingBox.name() : __accessibilityComputationAreaFromBoundingBox,
        __accessibilityComputationAreaFromNetwork.name() : __accessibilityComputationAreaFromNetwork
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', 'matsim_configType', matsim_configType)


# Complex type matsim4urbansim_configType with content type ELEMENT_ONLY
class matsim4urbansim_configType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'matsim4urbansim_configType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element matsim4urbansim uses Python identifier matsim4urbansim
    __matsim4urbansim = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'matsim4urbansim'), 'matsim4urbansim', '__AbsentNamespace0_matsim4urbansim_configType_matsim4urbansim', False)

    
    matsim4urbansim = property(__matsim4urbansim.value, __matsim4urbansim.set, None, None)

    
    # Element matsim_config uses Python identifier matsim_config
    __matsim_config = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'matsim_config'), 'matsim_config', '__AbsentNamespace0_matsim4urbansim_configType_matsim_config', False)

    
    matsim_config = property(__matsim_config.value, __matsim_config.set, None, None)


    _ElementMap = {
        __matsim4urbansim.name() : __matsim4urbansim,
        __matsim_config.name() : __matsim_config
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', 'matsim4urbansim_configType', matsim4urbansim_configType)


# Complex type matsim4urbansimType with content type ELEMENT_ONLY
class matsim4urbansimType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'matsim4urbansimType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element matsim4opus uses Python identifier matsim4opus
    __matsim4opus = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'matsim4opus'), 'matsim4opus', '__AbsentNamespace0_matsim4urbansimType_matsim4opus', False)

    
    matsim4opus = property(__matsim4opus.value, __matsim4opus.set, None, None)

    
    # Element year uses Python identifier year
    __year = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'year'), 'year', '__AbsentNamespace0_matsim4urbansimType_year', False)

    
    year = property(__year.value, __year.set, None, None)

    
    # Element matsim4opusConfig uses Python identifier matsim4opusConfig
    __matsim4opusConfig = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'matsim4opusConfig'), 'matsim4opusConfig', '__AbsentNamespace0_matsim4urbansimType_matsim4opusConfig', False)

    
    matsim4opusConfig = property(__matsim4opusConfig.value, __matsim4opusConfig.set, None, None)

    
    # Element backupRunData uses Python identifier backupRunData
    __backupRunData = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'backupRunData'), 'backupRunData', '__AbsentNamespace0_matsim4urbansimType_backupRunData', False)

    
    backupRunData = property(__backupRunData.value, __backupRunData.set, None, None)

    
    # Element matsim4opusOutput uses Python identifier matsim4opusOutput
    __matsim4opusOutput = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'matsim4opusOutput'), 'matsim4opusOutput', '__AbsentNamespace0_matsim4urbansimType_matsim4opusOutput', False)

    
    matsim4opusOutput = property(__matsim4opusOutput.value, __matsim4opusOutput.set, None, None)

    
    # Element opusDataPath uses Python identifier opusDataPath
    __opusDataPath = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'opusDataPath'), 'opusDataPath', '__AbsentNamespace0_matsim4urbansimType_opusDataPath', False)

    
    opusDataPath = property(__opusDataPath.value, __opusDataPath.set, None, None)

    
    # Element matsim4opusTemp uses Python identifier matsim4opusTemp
    __matsim4opusTemp = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'matsim4opusTemp'), 'matsim4opusTemp', '__AbsentNamespace0_matsim4urbansimType_matsim4opusTemp', False)

    
    matsim4opusTemp = property(__matsim4opusTemp.value, __matsim4opusTemp.set, None, None)

    
    # Element customParameter uses Python identifier customParameter
    __customParameter = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'customParameter'), 'customParameter', '__AbsentNamespace0_matsim4urbansimType_customParameter', False)

    
    customParameter = property(__customParameter.value, __customParameter.set, None, None)

    
    # Element parcelBasedAccessibility uses Python identifier parcelBasedAccessibility
    __parcelBasedAccessibility = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'parcelBasedAccessibility'), 'parcelBasedAccessibility', '__AbsentNamespace0_matsim4urbansimType_parcelBasedAccessibility', False)

    
    parcelBasedAccessibility = property(__parcelBasedAccessibility.value, __parcelBasedAccessibility.set, None, None)

    
    # Element populationSamplingRate uses Python identifier populationSamplingRate
    __populationSamplingRate = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'populationSamplingRate'), 'populationSamplingRate', '__AbsentNamespace0_matsim4urbansimType_populationSamplingRate', False)

    
    populationSamplingRate = property(__populationSamplingRate.value, __populationSamplingRate.set, None, None)

    
    # Element zone2ZoneImpedance uses Python identifier zone2ZoneImpedance
    __zone2ZoneImpedance = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'zone2ZoneImpedance'), 'zone2ZoneImpedance', '__AbsentNamespace0_matsim4urbansimType_zone2ZoneImpedance', False)

    
    zone2ZoneImpedance = property(__zone2ZoneImpedance.value, __zone2ZoneImpedance.set, None, None)

    
    # Element agentPerfomance uses Python identifier agentPerfomance
    __agentPerfomance = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'agentPerfomance'), 'agentPerfomance', '__AbsentNamespace0_matsim4urbansimType_agentPerfomance', False)

    
    agentPerfomance = property(__agentPerfomance.value, __agentPerfomance.set, None, None)

    
    # Element opusHome uses Python identifier opusHome
    __opusHome = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'opusHome'), 'opusHome', '__AbsentNamespace0_matsim4urbansimType_opusHome', False)

    
    opusHome = property(__opusHome.value, __opusHome.set, None, None)

    
    # Element zoneBasedAccessibility uses Python identifier zoneBasedAccessibility
    __zoneBasedAccessibility = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, 'zoneBasedAccessibility'), 'zoneBasedAccessibility', '__AbsentNamespace0_matsim4urbansimType_zoneBasedAccessibility', False)

    
    zoneBasedAccessibility = property(__zoneBasedAccessibility.value, __zoneBasedAccessibility.set, None, None)


    _ElementMap = {
        __matsim4opus.name() : __matsim4opus,
        __year.name() : __year,
        __matsim4opusConfig.name() : __matsim4opusConfig,
        __backupRunData.name() : __backupRunData,
        __matsim4opusOutput.name() : __matsim4opusOutput,
        __opusDataPath.name() : __opusDataPath,
        __matsim4opusTemp.name() : __matsim4opusTemp,
        __customParameter.name() : __customParameter,
        __parcelBasedAccessibility.name() : __parcelBasedAccessibility,
        __populationSamplingRate.name() : __populationSamplingRate,
        __zone2ZoneImpedance.name() : __zone2ZoneImpedance,
        __agentPerfomance.name() : __agentPerfomance,
        __opusHome.name() : __opusHome,
        __zoneBasedAccessibility.name() : __zoneBasedAccessibility
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', 'matsim4urbansimType', matsim4urbansimType)


matsim4urbansim_config = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'matsim4urbansim_config'), matsim4urbansim_configType)
Namespace.addCategoryObject('elementBinding', matsim4urbansim_config.name().localName(), matsim4urbansim_config)



fileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'inputFile'), pyxb.binding.datatypes.token, scope=fileType))
fileType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(fileType._UseForTag(pyxb.namespace.ExpandedName(None, 'inputFile')), min_occurs=1, max_occurs=1)
    )
fileType._ContentModel = pyxb.binding.content.ParticleModel(fileType._GroupModel, min_occurs=1, max_occurs=1)



matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'studyAreaBoundaryShapeFile'), fileType, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'boundingBoxLeft'), pyxb.binding.datatypes.double, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'boundingBoxRight'), pyxb.binding.datatypes.double, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'boundingBoxTop'), pyxb.binding.datatypes.double, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'boundingBoxBottom'), pyxb.binding.datatypes.double, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'urbansimZoneRandomLocationDistributionByRadius'), pyxb.binding.datatypes.double, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'urbansimZoneRandomLocationDistributionByShapeFile'), pyxb.binding.datatypes.token, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'external_matsim_config'), fileType, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'warmStartPlansFile'), fileType, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'useHotStart'), pyxb.binding.datatypes.boolean, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'hotStartPlansFile'), fileType, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'activityType_0'), pyxb.binding.datatypes.token, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'activityType_1'), pyxb.binding.datatypes.token, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'homeActivityTypicalDuration'), pyxb.binding.datatypes.nonNegativeInteger, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'workActivityTypicalDuration'), pyxb.binding.datatypes.nonNegativeInteger, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'workActivityOpeningTime'), pyxb.binding.datatypes.nonNegativeInteger, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'workActivityLatestStartTime'), pyxb.binding.datatypes.nonNegativeInteger, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'firstIteration'), pyxb.binding.datatypes.nonNegativeInteger, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'lastIteration'), pyxb.binding.datatypes.nonNegativeInteger, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'network'), fileType, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'cellSize'), pyxb.binding.datatypes.nonNegativeInteger, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'accessibilityComputationAreaFromShapeFile'), pyxb.binding.datatypes.boolean, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'accessibilityComputationAreaFromBoundingBox'), pyxb.binding.datatypes.boolean, scope=matsim_configType))

matsim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'accessibilityComputationAreaFromNetwork'), pyxb.binding.datatypes.boolean, scope=matsim_configType))
matsim_configType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, 'cellSize')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, 'accessibilityComputationAreaFromShapeFile')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, 'accessibilityComputationAreaFromBoundingBox')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, 'accessibilityComputationAreaFromNetwork')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, 'studyAreaBoundaryShapeFile')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, 'boundingBoxTop')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, 'boundingBoxLeft')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, 'boundingBoxRight')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, 'boundingBoxBottom')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, 'urbansimZoneRandomLocationDistributionByRadius')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, 'urbansimZoneRandomLocationDistributionByShapeFile')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, 'external_matsim_config')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, 'network')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, 'warmStartPlansFile')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, 'useHotStart')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, 'hotStartPlansFile')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, 'activityType_0')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, 'activityType_1')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, 'homeActivityTypicalDuration')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, 'workActivityTypicalDuration')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, 'workActivityOpeningTime')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, 'workActivityLatestStartTime')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, 'firstIteration')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim_configType._UseForTag(pyxb.namespace.ExpandedName(None, 'lastIteration')), min_occurs=1, max_occurs=1)
    )
matsim_configType._ContentModel = pyxb.binding.content.ParticleModel(matsim_configType._GroupModel, min_occurs=1, max_occurs=1)



matsim4urbansim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'matsim4urbansim'), matsim4urbansimType, scope=matsim4urbansim_configType))

matsim4urbansim_configType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'matsim_config'), matsim_configType, scope=matsim4urbansim_configType))
matsim4urbansim_configType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(matsim4urbansim_configType._UseForTag(pyxb.namespace.ExpandedName(None, 'matsim_config')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansim_configType._UseForTag(pyxb.namespace.ExpandedName(None, 'matsim4urbansim')), min_occurs=1, max_occurs=1)
    )
matsim4urbansim_configType._ContentModel = pyxb.binding.content.ParticleModel(matsim4urbansim_configType._GroupModel, min_occurs=1, max_occurs=1)



matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'matsim4opus'), pyxb.binding.datatypes.token, scope=matsim4urbansimType))

matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'year'), pyxb.binding.datatypes.nonNegativeInteger, scope=matsim4urbansimType))

matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'matsim4opusConfig'), pyxb.binding.datatypes.token, scope=matsim4urbansimType))

matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'backupRunData'), pyxb.binding.datatypes.boolean, scope=matsim4urbansimType))

matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'matsim4opusOutput'), pyxb.binding.datatypes.token, scope=matsim4urbansimType))

matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'opusDataPath'), pyxb.binding.datatypes.token, scope=matsim4urbansimType))

matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'matsim4opusTemp'), pyxb.binding.datatypes.token, scope=matsim4urbansimType))

matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'customParameter'), pyxb.binding.datatypes.token, scope=matsim4urbansimType))

matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'parcelBasedAccessibility'), pyxb.binding.datatypes.boolean, scope=matsim4urbansimType))

matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'populationSamplingRate'), pyxb.binding.datatypes.double, scope=matsim4urbansimType))

matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'zone2ZoneImpedance'), pyxb.binding.datatypes.boolean, scope=matsim4urbansimType))

matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'agentPerfomance'), pyxb.binding.datatypes.boolean, scope=matsim4urbansimType))

matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'opusHome'), pyxb.binding.datatypes.token, scope=matsim4urbansimType))

matsim4urbansimType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'zoneBasedAccessibility'), pyxb.binding.datatypes.boolean, scope=matsim4urbansimType))
matsim4urbansimType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, 'populationSamplingRate')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, 'year')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, 'opusHome')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, 'opusDataPath')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, 'matsim4opus')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, 'matsim4opusConfig')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, 'matsim4opusOutput')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, 'matsim4opusTemp')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, 'customParameter')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, 'zone2ZoneImpedance')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, 'agentPerfomance')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, 'zoneBasedAccessibility')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, 'parcelBasedAccessibility')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(matsim4urbansimType._UseForTag(pyxb.namespace.ExpandedName(None, 'backupRunData')), min_occurs=1, max_occurs=1)
    )
matsim4urbansimType._ContentModel = pyxb.binding.content.ParticleModel(matsim4urbansimType._GroupModel, min_occurs=1, max_occurs=1)
