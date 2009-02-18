#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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
##IGNORE_THIS_FILE

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from opus_gui.results_manager.views.ui_mapnik_options_dialog import Ui_Dialog


class MapOptions(QDialog, Ui_Dialog):
    def __init__(self, parent = None, options_dict = None): #deleted: project = None, viz_name = 'default visualization name', 
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.show()
        self.connect(self.pb_applyChanges, SIGNAL("clicked()"), self.applyChanges(options_dict))
        self.loadXML(options_dict)
        self.initWindow(options_dict)

    def initWindow(self, options_dict):
        if (options_dict['bucket_ranges'] == 'linear_scale'):
            self.cb_colorScalingType.setCurrentIndex(0)
        else:
            self.cb_colorScalingType.setCurrentIndex(1)
            self.le_customScale.setText(QString(options_dict['bucket_ranges']))
            
        if (options_dict['bucket_labels'] == 'range_labels'):
            self.cb_labelType.setCurrentIndex(0)
        else:
            self.cb_labelType.setCurrentIndex(1)
            self.le_customLabels.setText(QString(options_dict['bucket_labels']))
            
        self.cb_NumColRanges.setCurrentIndex(10-self.num_buckets)
        
        self.setRangeColumn(options_dict)
        self.setLabelColumn()
        self.setColorColumn()

    def applyChanges(self, options_dict):
        def applyChangesHelper():
            self.setColorTableRows(options_dict)
            self.writeXML(options_dict)
        return applyChangesHelper
    
    def setColorTableRows(self, options_dict):
        """ set the rows of the color table """
        self.num_buckets = int(self.cb_NumColRanges.currentText())
        self.tbl_Colors.setRowCount (self.num_buckets)
        
        self.setRangeList(options_dict)
        self.setRangeColumn(options_dict)
        
        self.setLabelList(options_dict)
        self.setLabelColumn()
            
        self.setColorList()
        self.setColorColumn()
        
    def setRangeColumn(self, options_dict):
        if (options_dict['bucket_ranges'] == 'linear_scale'):
            for i in range(self.num_buckets):
                if i == 0:
                    input_str = 'MIN'
                elif i == self.num_buckets-1:
                    input_str = 'MAX'
                else:
                    input_str = ''
                if (self.tbl_Colors.item(i, 1)):
                    self.tbl_Colors.item(i, 1).setText(input_str)
                else:
                    self.tbl_Colors.setItem(i, 1, QTableWidgetItem(input_str))
        else:
            self.range_list = self.range_list[0:self.num_buckets+1]
            for i in range(self.num_buckets):
                if i < self.range_list.__len__()-1:
                    input_str = str(self.range_list[i]).strip() + " to " + str(self.range_list[i+1]).strip()
                else:
                    input_str = ''
                if (self.tbl_Colors.item(i, 1)):
                    self.tbl_Colors.item(i, 1).setText(input_str)
                else:
                    self.tbl_Colors.setItem(i, 1, QTableWidgetItem(input_str))
                    
    def setLabelColumn(self):
        self.label_list = self.label_list[0:self.num_buckets]
        for i in range(self.num_buckets):
            if i < self.label_list.__len__():
                input_str = str(self.label_list[i]).strip()
            else:
                input_str = ''
            if (self.tbl_Colors.item(i,2)):
                self.tbl_Colors.item(i, 2).setText(input_str)
            else:
                self.tbl_Colors.setItem(i, 2, QTableWidgetItem (input_str))

    def setColorColumn(self):
        self.color_list = self.color_list[0:self.num_buckets]
        for i in range(self.color_list.__len__()):
            colorPB = QPushButton()
            colorPB.setStyleSheet("QWidget { background-color: %s }" % self.color_list[i])
            colorPB.connect(colorPB, SIGNAL('clicked()'), self.makeChooseColor(colorPB,i))
            self.tbl_Colors.setCellWidget(i,0,colorPB)
    
    def setRangeList(self, options_dict):
        if (self.cb_colorScalingType.currentText() == 'Linear Scaling'):
            options_dict['bucket_ranges'] = 'linear_scale'
        elif(self.cb_colorScalingType.currentText() == 'Custom Scaling'): # use the custom scale
            self.range_list = str(self.le_customScale.text()).split(',')
            options_dict['bucket_ranges'] = self.listToString(self.range_list)
            
    def setLabelList(self, options_dict):
        if (self.cb_labelType.currentText() == 'Range Values'):
            options_dict['bucket_labels'] = 'range_labels'
            self.setLabelListForRangeValues(options_dict)
        elif (self.cb_labelType.currentText() == 'Custom Labels'): # use the custom scale
            self.label_list = str(self.le_customLabels.text()).split(',')
            options_dict['bucket_labels'] = self.listToString(self.label_list)
        
    def setColorList(self):
        color_scheme_sel = self.cb_colorScheme.currentText()
        divergeIndex = self.cb_divergeIndex.currentIndex()
                
        if (color_scheme_sel == 'Green' or color_scheme_sel == 'Red' or color_scheme_sel == 'Blue'):
            from numpy import array
            pre_defined_green = array( ['#e0eee0', '#c7e9c0', '#a1d99b', '#7ccd7c', '#74c476', '#41ab5d', '#238b45', '#006400', '#00441b', '#00340b'] ) 
            pre_defined_red = array( ['#fee0d2', '#fcbba1', '#fc9272', '#fb6a4a', '#ef3b2c', '#cb181d', '#b0171f', '#a50f15',  '#67000d', '#400000'] )
            pre_defined_blue = array( ['#deebf7', '#c6dbef',  '#b9d3ee', '#9ecae1', '#6baed6', '#4292c6', '#2171b5', '#08519c', '#08306b', '#011561'] )
    
            self.color_list = []
    
            if (color_scheme_sel == 'Green'):
                color_array = pre_defined_green
            elif (color_scheme_sel == 'Red'):
                color_array = pre_defined_red
            else: # (color_scheme_sel == 'Blue'):
                color_array = pre_defined_blue

            from math import ceil
            neg_val_color_scheme = self.cb_colorSchemeNeg.currentText()
            if (neg_val_color_scheme == 'Green'):
                neg_color_array = pre_defined_green
            elif (neg_val_color_scheme == 'Blue'):
                neg_color_array = pre_defined_blue
            else: # (neg_val_color_scheme == 'Red'):
                neg_color_array = pre_defined_red
            # set lower range colors
            for i in range(1, divergeIndex):
                self.color_list.append(neg_color_array[int(10-ceil(10.0*i/(divergeIndex)))])
            # set the zero color
            if (divergeIndex != 0):
                self.color_list.append('#ffffff')
            # set the upper range colors
            num_pos = self.num_buckets-divergeIndex+1
            for i in range(1, num_pos):
                self.color_list.append(color_array[int(10.0*i/(num_pos))])
    
        else: # (color_scheme_sel == 'Custom Color Scheme' or color_scheme_sel == 'Custom Graduated Colors')
            self.updateColorList()
            if (color_scheme_sel == 'Custom Graduated Colors'):
                start_color = self.color_list[0]
                end_color = self.color_list[self.num_buckets-1]
                if (divergeIndex == 0):
                    self.color_list = self.getGraduatedColorsList(start_color, end_color, self.num_buckets)
                else:
                    self.color_list = self.getGraduatedColorsList(start_color, '#ffffff', divergeIndex)
                    self.color_list.__delitem__(self.color_list.__len__()-1) # remove '#ffffff' from color_list because it will be re-added
                    self.color_list = self.color_list.__add__(self.getGraduatedColorsList('#ffffff', end_color, self.num_buckets-divergeIndex+1))
    
    def getGraduatedColorsList(self, start_color, end_color, list_len):
        grad_color_list = []
        
        if (list_len > 0):
            red_start = int(str(start_color[1:3]),16)
            green_start = int(str(start_color[3:5]),16)
            blue_start = int(str(start_color[5:7]),16)
            
            red_end = int(str(end_color[1:3]),16)
            green_end = int(str(end_color[3:5]),16)
            blue_end = int(str(end_color[5:7]),16)
            
            red_slope = (red_end -  red_start) / list_len
            green_slope = (green_end - green_start) / list_len
            blue_slope = (blue_end - blue_start) / list_len
            
            
            grad_color_list.append(start_color)
            for i in range(1,list_len-1):
                grad_color_list.append('#'+self.decColorToHexColor(red_start+red_slope*i)+self.decColorToHexColor(green_start+green_slope*i)+self.decColorToHexColor(blue_start+blue_slope*i))
            grad_color_list.append(end_color)
        
        return grad_color_list

    def decColorToHexColor(self, dec_val):
        hex = __builtins__['hex']        
        hex_val = hex(dec_val)
        if hex_val.__len__() == 3: # hex_val has a single digit
            return '0'+hex_val[hex_val.__len__()-1:]
        else: # hex_val has more than one digits
            return hex_val[hex_val.__len__()-2:]

    def makeChooseColor(self, pb, index):
        def chooseAndSaveColor():
            self.color_list[index] = QColorDialog.getColor().name()
            pb.setStyleSheet("QWidget { background-color: %s }" % self.color_list[index])
        return chooseAndSaveColor 

    def setLabelListForRangeValues(self, options_dict):
        self.label_list = []
        if (options_dict['bucket_ranges'] == 'linear_scale'):
            self.label_list.append('MIN')
            while (self.label_list.__len__() < self.num_buckets-1):
                self.label_list.append('')
            self.label_list.append('MAX')
        else:
            for i in range(self.range_list.__len__()-1):
                self.label_list.append(self.range_list[i] + " to " + self.range_list[i+1])

    def updateColorList(self):
        # if colors need to be removed from the color list:
        if (self.num_buckets < self.color_list.__len__()):
            self.color_list = self.color_list[:self.num_buckets]   
        # if color buttons need to be added:
        for i in range(self.num_buckets):
            default_color = '#ffffff'
            if (not self.tbl_Colors.cellWidget(i, 0)):
                self.color_list.append(default_color)
                self.makeColorButton(i, default_color)
                
    def makeColorButton(self, row, color=None):
        colorPB = QPushButton()
        if (not color is None):
            colorPB.setStyleSheet("QWidget { background-color: %s }" % color)
        colorPB.connect(colorPB, SIGNAL('clicked()'), self.makeChooseColor(colorPB,row))
        self.tbl_Colors.setCellWidget(row,0,colorPB)
        
    def listToString(self, list):
        text = ''
        for i in range(list.__len__()-1):
            text += str(list[i]).strip() + ','
        if list.__len__() > 0:
            text += list[list.__len__() -1]
        return text
    
    def stringToList(self, string):
        list = string.split(',')
        for i in range(list.__len__()):
            list[i] = str(list[i]).strip()
        return list
    
    def writeXML(self, options_dict): 
        options_dict['bucket_colors'] = self.listToString(self.color_list)
        if options_dict['bucket_ranges'] != 'linear_scale':
            options_dict['bucket_ranges'] = self.listToString(self.range_list)
        if options_dict['bucket_labels'] != 'range_labels':
            options_dict['bucket_labels'] = self.listToString(self.label_list)

    def loadXML(self, options_dict):
        self.color_list = self.stringToList(options_dict['bucket_colors'])
        self.num_buckets = self.color_list.__len__()
        self.range_list = self.stringToList(options_dict['bucket_ranges']) # if not a list, will just be single string
        if options_dict['bucket_labels'] == 'range_labels':
            self.setLabelListForRangeValues(options_dict)
        else:
            self.label_list = self.stringToList(options_dict['bucket_labels'])
        

from opus_core.tests import opus_unittest
import opus_gui.results_manager.run.get_mapnik_options

class MapOptionsTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.app = QApplication([])
        self.window = QMainWindow()
        
        self.range_str = '0,100,200,300,400,500'
        self.color_str = '#e0eee0,#a1d99b,#74c476,#238b45,#00441b'
        self.label_str = '0 to 100,100 to 200,200 to 300,300 to 400,400 to 500'
        
        self.range_lst = ['0', '100', '200', '300', '400', '500']
        self.color_lst = ['#e0eee0', '#a1d99b', '#74c476', '#238b45', '#00441b']
        self.label_lst = ['0 to 100', '100 to 200', '200 to 300', '300 to 400', '400 to 500']
        
        self.options_dict = {}
        self.options_dict['bucket_ranges'] = self.range_str
        self.options_dict['bucket_colors'] = self.color_str
        self.options_dict['bucket_labels'] = self.label_str
        self.mapOptionsInst = MapOptions(parent=self.window, options_dict=self.options_dict)
        
    def test_setRangeColumn(self):
        # setRangeColumn() is called in the setUp() as part of the init function
        # so check to make sure all items in the range column were set correctly
        for i in range(self.mapOptionsInst.num_buckets):
            self.assertEqual(self.mapOptionsInst.tbl_Colors.item(i, 1).text(), self.label_lst[i])
        # test that custom ranges are set correctly
        self.mapOptionsInst.range_list = ['0','1','2','3','4','5']
        self.mapOptionsInst.setRangeColumn(self.options_dict)
        for i in range(self.mapOptionsInst.num_buckets-1):
            self.assertEqual(str(self.mapOptionsInst.tbl_Colors.item(i, 1).text()), self.mapOptionsInst.range_list[i] + ' to ' + self.mapOptionsInst.range_list[i+1])
        # test that linear range is set correctly
        self.options_dict['bucket_ranges'] = 'linear_scale'
        self.mapOptionsInst.setRangeColumn(self.options_dict)
        for i in range(self.mapOptionsInst.num_buckets):
            if (i == 0):
                expected_val = 'MIN'
            elif (i == self.mapOptionsInst.num_buckets-1):
                expected_val = 'MAX'
            else:
                expected_val = ''
            self.assertEqual(str(self.mapOptionsInst.tbl_Colors.item(i,1).text()), expected_val)
        
    def test_SetLabelColumn(self):
        # setLabelColumn() is called in the setUp() as part of the init function
        # so check to make sure all items in the label column were set correctly
        for i in range(self.mapOptionsInst.num_buckets):
            self.assertEqual(self.mapOptionsInst.tbl_Colors.item(i, 2).text(), self.label_lst[i])
        # test that custom labels are set correctly
        self.mapOptionsInst.label_list = ['a','b','c','d','e']
        self.mapOptionsInst.setLabelColumn()
        for i in range(self.mapOptionsInst.num_buckets):
            self.assertEqual(str(self.mapOptionsInst.tbl_Colors.item(i, 2).text()), self.mapOptionsInst.label_list[i])
    
    def test_setColorColumn(self):
        # setColorColumn() is called in the setUp() as part of the init function
        # so check to make sure the color_list was set correctly
        self.assertEqual(self.mapOptionsInst.color_list, self.color_lst)
    
    def test_makeColorButton(self):
        self.mapOptionsInst.tbl_Colors.clear()
        for i in range(10):
            self.mapOptionsInst.makeColorButton(i, '#ffffff')
            self.assertNotEqual(self.mapOptionsInst.tbl_Colors.cellWidget(i, 0), None)
    
    def test_setLabelListForRangeValues(self):
        self.mapOptionsInst.setLabelListForRangeValues(self.options_dict)
        self.assertEqual(self.mapOptionsInst.label_list, self.label_lst)
        
        self.options_dict['bucket_ranges'] = 'linear_scale'
        self.mapOptionsInst.setLabelListForRangeValues(self.options_dict)
        self.assertEqual(self.mapOptionsInst.label_list, ['MIN', '', '', '', 'MAX'])
    
    def test_updateColorList(self):
        default_color = '#ffffff'
        # test case: colors need to be removed from color_list
        self.mapOptionsInst.color_list.append(default_color)
        self.mapOptionsInst.updateColorList()
        self.assertEqual(self.mapOptionsInst.color_list.__len__(), self.mapOptionsInst.num_buckets)
        # test case: colors need to be added to color_list
        self.mapOptionsInst.color_list = []
        self.mapOptionsInst.tbl_Colors.clear()
        self.mapOptionsInst.num_buckets = 10
        self.mapOptionsInst.updateColorList()
        for i in range(10):
            self.assertEqual(self.mapOptionsInst.color_list[i], default_color)
            self.assertNotEqual(self.mapOptionsInst.tbl_Colors.cellWidget(i, 0), None)
    
    def test_setRangeList(self):
        linear_scaling = 0
        custom_scaling = 1
        self.mapOptionsInst.cb_colorScalingType.setCurrentIndex(linear_scaling)
        self.mapOptionsInst.setRangeList(self.options_dict)
        self.assertEqual(self.options_dict['bucket_ranges'], 'linear_scale')
        
        self.mapOptionsInst.cb_colorScalingType.setCurrentIndex(custom_scaling)
        self.mapOptionsInst.le_customScale.setText(QString(self.range_str))
        self.mapOptionsInst.setRangeList(self.options_dict)
        self.assertEqual(self.options_dict['bucket_ranges'], self.range_str)
    
    def test_setLabelList(self):
        range_values = 0
        custom_labels = 1
        self.mapOptionsInst.cb_labelType.setCurrentIndex(range_values)
        self.mapOptionsInst.setLabelList(self.options_dict)
        self.assertEqual(self.options_dict['bucket_labels'], 'range_labels')
    
        self.mapOptionsInst.cb_labelType.setCurrentIndex(custom_labels)
        self.mapOptionsInst.le_customScale.setText(QString(self.label_str))
        self.mapOptionsInst.setLabelList(self.options_dict)
        self.assertEqual(self.options_dict['bucket_labels'], self.label_str)
    
    def test_writeXML(self):
        self.mapOptionsInst.writeXML(self.options_dict)
        self.assertEqual(self.options_dict['bucket_colors'], self.color_str)
        self.assertEqual(self.options_dict['bucket_ranges'], self.range_str)
        self.assertEqual(self.options_dict['bucket_labels'], self.label_str)
        
    def test_loadXML(self):
        self.mapOptionsInst.loadXML(self.options_dict)
        self.assertEqual(self.mapOptionsInst.range_list, self.range_lst)
        self.assertEqual(self.mapOptionsInst.color_list, self.color_lst)
        self.assertEqual(self.mapOptionsInst.label_list, self.label_lst)
        
    def test_listToString(self):
        self.assertEqual(self.mapOptionsInst.listToString(['']),'')
        self.assertEqual(self.mapOptionsInst.listToString(self.range_lst),self.range_str)
        
    def test_stringToList(self):
        self.assertEqual(self.mapOptionsInst.stringToList(''),[''])
        self.assertEqual(self.mapOptionsInst.stringToList(self.range_str),self.range_lst)


if __name__ == '__main__':
    opus_unittest.main()
