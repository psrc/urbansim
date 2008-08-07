# UrbanSim software. Copyright (C) 1998-2008 University of Washington
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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtXml import *


#################### Basic XML Node/Element Helpers #######################

## Get node text
def getNodeText(qDomNode):
    if not qDomNode or qDomNode.isNull():
        return None
    # Make sure that we have a qDomElement
    if qDomNode.isElement():
        qDomElement = qDomNode.toElement()
        if not qDomElement.isNull():
            return getElementText(qDomElement)
    return None
    
## Get element text
def getElementText(qDomElement):
    if not qDomElement or qDomElement.isNull():
        return None
    # Make sure that we have a qDomElement
    if qDomElement.nodeType() == QDomNode.ElementNode:
        # Grab the text
        return qDomElement.text()
    return None


## Find elements by type attribute returned in a list
def getElementsByType(qDomNode, eType, multiple=False, recursive=False):
    returnList = []
    if qDomNode and qDomNode.hasChildNodes():
        children = qDomNode.childNodes()
        for x in xrange(0,children.count(),1):
            if children.item(x).isElement():
                child = children.item(x).toElement()
                if child.hasAttribute(QString("type")) and \
                       (child.attribute(QString("type")) == eType):
                    returnList.append(child)
                    if multiple == False:
                        break
                if recursive and child.hasChildNodes():
                    returnList.extend(getElementsByType(child, eType, multiple, recursive))
    return returnList

## Find elements by tagname returned in a list
def getElementsByTagname(qDomNode, eTag, multiple=False, recursive=False):
    returnList = []
    if qDomNode and qDomNode.hasChildNodes():
        children = qDomNode.childNodes()
        for x in xrange(0,children.count(),1):
            if children.item(x).isElement():
                childElement = children.item(x).toElement()
                if childElement.tagName() == eTag:
                    returnList.append(childElement)
                    if multiple == False:
                        break
                if recursive and childElement.hasChildNodes():
                    returnList.extend(getElementsByTagname(childElement, eTag, multiple, recursive))
    return returnList


## Get all of the text values for a set of child nodes in a dict
## An eTagList of [] will get all elements, first indicates keep the first occurance
## if multiple are encountered, and recursive looks deep.
def getChildElementsText(qDomNode, eTagList=[], first=False, recursive=False):
    returnDict = {}
    if (not qDomNode) or (qDomNode.isNull()):
        return returnDict
    childNode = qDomNode.firstChild()
    while not childNode.isNull():
        if (eTagList == []) or (childNode.nodeName() in eTagList):
            if childNode.isElement():
                qDomElement = childNode.toElement()
                if not qDomElement.isNull():
                    # We need to check if we are overwritting an existing node... and check the first param
                    if (not first) or not (qDomElement.tagName() in returnDict):
                        returnDict[qDomElement.tagName()] = qDomElement.text()
        if recursive and childNode.hasChildNodes():
            if first:
                tempDict = getChildElementsText(childNode, eTagList, first, recursive)
                tempDict.update(returnDict)
                returnDict = tempDict
            else:
                returnDict.update(getChildElementsText(childNode, eTagList, first, recursive))
        childNode = childNode.nextSibling()
    return returnDict


#################### Opus XML Helpers #######################


#################### Unit Tests for XML Helpers ###########################

from opus_core.tests import opus_unittest
import os

class XMLHelperTests(opus_unittest.OpusTestCase):
    def setUp(self):
        # find the directory containing the test xml configurations
        opus_gui_dir = __import__('opus_gui').__path__[0]
        self.test_configs = os.path.join(opus_gui_dir, 'utils')
        self.test_xml = """
<opus_project>
  <data_manager>
    <Tool_Library type="tool_library" setexpanded="True" >
      <tool_path flags="hidden" type="tool_path" >tools</tool_path>
      <shapefile_to_postgis type="tool_file">
        <name type="tool_name">shapefile_to_postgis</name>
        <params type="param_template">
          <dbname type="string">
	    <required choices="Required|Optional" type="string">Required</required>
	    <type choices="string" type="string">string</type>
	    <default type="string">1</default>
	  </dbname>
          <schema_name>
	    <required choices="Required|Optional" type="string">Required</required>
	    <type choices="string" type="string">string</type>
	    <default type="string"></default>
	  </schema_name>
          <shapefile_path>
	    <required choices="Required|Optional" type="string">Required</required>
	    <type choices="file_path" type="string">file_path</type>
	    <default type="file_path"></default>
	  </shapefile_path>
          <output_table_name>
	    <required choices="Required|Optional" type="string">Required</required>
	    <type choices="string" type="string">string</type>
	    <default type="string"></default>
	  </output_table_name>
          <geometry_type>
	    <required choices="Required|Optional" type="string">Optional</required>
	    <type choices="string" type="string">string</type>
	    <default choices="NONE|GEOMETRY|POINT|LINESTRING|POLYGON" type="string">NONE</default>
	  </geometry_type>
          <overwrite>
	    <required choices="Required|Optional" type="string">Optional</required>
	    <type choices="string" type="string">string</type>
	    <default choices="YES|NO" type="string">NO</default>
	  </overwrite>
        </params>
      </shapefile_to_postgis>
    </Tool_Library>
  </data_manager>
</opus_project>
        """

    def test_getNodeText(self):
        qDomDocument = QDomDocument()
        qDomDocument.setContent(QString(self.test_xml))
        projectNodes = qDomDocument.elementsByTagName(QString('opus_project'))
        self.assertNotEqual(projectNodes.isEmpty(),True)
        projectNode = projectNodes.item(0)

        # This should be the tool_path
        child = projectNode.firstChild().firstChild().firstChild()
        text = getNodeText(child)
        self.assertEqual(text,QString('tools'))
        self.assertEqual(getNodeText(QDomNode()),None)
        self.assertEqual(getNodeText(None),None)
        

    def test_getElementText(self):
        qDomDocument = QDomDocument()
        qDomDocument.setContent(QString(self.test_xml))
        projectNodes = qDomDocument.elementsByTagName(QString('opus_project'))
        self.assertNotEqual(projectNodes.isEmpty(),True)
        projectNode = projectNodes.item(0)

        # Try to get the text from a node
        elementList = getElementsByType(projectNode,QString('tool_name'),multiple=False,recursive=True)
        self.assertEqual(len(elementList),1)
        self.assertEqual(getElementText(elementList[0]),QString('shapefile_to_postgis'))

        # Test a bad element
        elementBad = QDomElement()
        self.assertEqual(getElementText(elementBad),None)
        self.assertEqual(getElementText(None),None)
        

    def test_getElementsByType(self):
        qDomDocument = QDomDocument()
        qDomDocument.setContent(QString(self.test_xml))
        projectNodes = qDomDocument.elementsByTagName(QString('opus_project'))
        self.assertNotEqual(projectNodes.isEmpty(),True)
        projectNode = projectNodes.item(0)
        
        # Try to get first occurance of type 'default'
        elementList = getElementsByType(projectNode,QString('tool_name'),multiple=False,recursive=True)
        self.assertEqual(len(elementList),1)
        self.assertEqual(elementList[0].attribute(QString('type')),QString('tool_name'))
        self.assertEqual(elementList[0].text(),QString('shapefile_to_postgis'))

    def test_getElementsByTagname(self):
        qDomDocument = QDomDocument()
        qDomDocument.setContent(QString(self.test_xml))
        projectNodes = qDomDocument.elementsByTagName(QString('opus_project'))
        self.assertNotEqual(projectNodes.isEmpty(),True)
        projectNode = projectNodes.item(0)

        # Try to get first occurance of 'default'
        elementList = getElementsByTagname(projectNode,QString('tool_path'),multiple=False,recursive=True)
        self.assertEqual(len(elementList),1)
        self.assertEqual(elementList[0].tagName(),QString('tool_path'))

        # Now try to recurse and test
        elementList = getElementsByTagname(projectNode,QString('required'),multiple=True,recursive=True)
        self.assertEqual(len(elementList),6)
        self.assertEqual(elementList[0].text(),QString('Required'))
        self.assertEqual(elementList[-1].text(),QString('Optional'))
        

    def test_getChildElementsText(self):
        qDomDocument = QDomDocument()
        qDomDocument.setContent(QString(self.test_xml))
        projectNodes = qDomDocument.elementsByTagName(QString('opus_project'))
        self.assertNotEqual(projectNodes.isEmpty(),True)
        projectNode = projectNodes.item(0)
        toolsToTest = getElementsByType(projectNode,QString('tool_file'),recursive=True)
        self.assertNotEqual(len(toolsToTest),0)
        toolToTest = toolsToTest[0]
        self.assertEqual(toolToTest.tagName(), QString('shapefile_to_postgis'))

        # Grab the name of the tool... should just be one
        returnDict = getChildElementsText(toolToTest,[QString('name')])
        self.assertEqual(returnDict, {QString('name'):QString('shapefile_to_postgis')})

        # Recurse and grab all of the default values... but only keep the first
        returnDict = getChildElementsText(toolToTest,[QString('default')],first=True,recursive=True)
        self.assertEqual(len(returnDict), 1)
        self.assertEqual(str(returnDict[QString('default')]), '1')

        # Recurse and grab all of the default values... but only keep the last
        returnDict = getChildElementsText(toolToTest,[QString('default')],first=False,recursive=True)
        self.assertEqual(len(returnDict), 1)
        self.assertEqual(returnDict[QString('default')], QString('NO'))

        # DONT Recurse and grab all of the default values... should be 0
        returnDict = getChildElementsText(toolToTest,[QString('default')],first=False,recursive=False)
        self.assertEqual(len(returnDict), 0)

if __name__ == '__main__':
    opus_unittest.main()



