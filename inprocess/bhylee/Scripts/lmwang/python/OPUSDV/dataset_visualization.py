#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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

NODATA = -1

import configure_path
from resources import Resources
import Numeric as numpy
import numarray as na
from dataset import DataSet, SetAttribute

class DataSetVisualization:
    """Visualization for instance of dataset class"""
    
    def __init__(self, dataset, display_attribute, engine_name = "matplotlib"):
        """
        The argument 'dataset' is an instance of class DataSet, and it must have a unique combination of 
        relative_x and relative_y fields. 'display_attribute' is an attribute in dataset whose value is used
        to show in the map. 'engine_name' is the name of one of the implemented VisualizationEngines 
        """
        if isinstance(dataset, GridcellSet):
            self.display_2d_array = dataset.get_2d_attribute(display_attribute)
        elif isinstance(dataset, DataSet):
            try:
                relative_x = dataset.get_attribute('relative_x')
                relative_y = dataset.get_attribute('relative_y')
                display_value = dataset.get_attribute(display_attribute)
            except AttributeError:
                AttributeError, "dataset must include attributes relative_x, relative_y, and " + display_value + "."
            
            self.display_2d_array = na.zeros((int(relative_x.max()),int(relative_y.max()))) + NODATA
            self.display_2d_array[relative_x-1, relative_y-1] = display_value
        else:
            raise TypeError, "dataset must be of type DataSet defined in OpusCore."
        
        self.engine_name = engine_name
        
    def display(self):
        """
        Display self.display_2d_array
        """
        engine = VisualizationEngineFactory().factory(self.engine_name, self.display_2d_array)
        engine.display()
        
class VisualizationEngineFactory:
    def factory(self, engine, object):
        if engine == "matplotlib":
            return MatplotlibEngine(object)
        elif engine == "Thuban":
            return ThubanEngine(object)
        elif engine == "OpenEV":
            return OpenEVEngine(object)
        elif engine == "FloatCanvas":
            return FloatCanvasEngine(object)
        else:
            raise RuntimeWarning, "Unsupported VisualizationEngine: " + engine + "."

class VisualizationEngine:
    """Super class for various visualization engines, including MatplotlibEngine, ThubanEngine, etc"""
    def __init__(self, object):
        #if not isinstance(object, na.NumArray):
        #    raise TypeError, "object must be of type NumArray"
        self.object = convert_numarray_to_numeric_array(object)    
        self.object = numpy.transpose(self.object)

    def display(self):
        pass
    
    def close(self):
        pass

class MatplotlibEngine(VisualizationEngine):
    def __init__(self, object):
        VisualizationEngine.__init__(self,object)
        
    def display(self):
        try:
            from matplotlib.pylab import *
        except:
            ImportError, "Unable to import Module matplotlib."
        
        im = figimage(self.object, cmap=cm.gray, vmin=1, vmax=72)
        #(w,h) = figaspect(self.object)
        #fig = Figure(figsize=(w,h))
        #ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
        #ax.imshow(self.object)
        axis('off'); #colorbar(); 
        show()

class ThubanEngine(VisualizationEngine):
    def __init__(self, object):
        VisualizationEngine.__init__(self,object)

    def display(self):
        try:
            #import gdal,_gdal
            import gdalnumeric
        except:
            ImportError, "Unable to import Module gdalnumeric."
        
        imgds = gdalnumeric.OpenArray(self.object)
        pass
        

class OpenEVEngine(VisualizationEngine):
    def __init__(self, object):
        VisualizationEngine.__init__(self,object)
    
    def display(self):
        try:
            import gdalnumeric
            import gview
            import gviewapp
            import gtk
        except:
            raise ImportError, "Unable to import Module gdalnumeric, gview and gviewapp."
        
        if os.path.isdir(os.path.join(gview.home_dir, 'config')):
            mfile = os.path.join(gview.home_dir, 'config', 'DefaultMenuFile.xml')
            ifile = os.path.join(gview.home_dir, 'config', 'DefaultIconFile.xml')
            pfile = os.path.join(gview.home_dir, 'config', 'DefaultPyshellFile.xml')
        else:
            mfile=None
            ifile=None
            pfile=None
         
        tfile = None
        
        app = gviewapp.GViewApp(toolfile=tfile,menufile=mfile,iconfile=ifile,pyshellfile=pfile)
        gview.app = app
        app.subscribe('quit',gtk.mainquit)   # connect to gtk's quit mechanism
        app.show_layerdlg()                  # show layer dialog
        app.new_view(None)                  # create initial view window
        app.do_auto_imports()
        
        imgds = gdalnumeric.OpenArray(self.object)
        imgraster = gview.GvRaster(dataset=imgds)
        imgrlayer = gview.GvRasterLayer(raster=imgraster)

        aview = gview.app.sel_manager.get_active_view()
        aview.add_layer(imgrlayer)

        gtk.mainloop()         # start the main event loop
        
class FloatCanvasEngine(VisualizationEngine):
    def __init__(self, object):
        VisualizationEngine.__init__(self,object)
    
    def display(self):
        try:
            from wxPython.lib import floatcanvas
        except:
            ImportError, "Unable to import Module flocatcanvas."
        pass

def prepare_dataset(dataset, display_attribute, loc_dataset=None):
    pass

def convert_numarray_to_numeric_array(na_array):
    return numpy.array(na_array.tolist(), typecode=na_array.typecode())

import os, sys
import unittest
from store.storage_creator import StorageCreator
from gridcellset.gridcells import GridcellSet

class DataSetVisualizationTest(unittest.TestCase):
    dirEugene = os.environ['OPUSHOME'] + "/UrbanSim4/data/flt/Eugene_1980_baseyear"
    storage_dictionary = Resources({"base":dirEugene})
    in_storage = StorageCreator().get_storage("Flt", storage_dictionary)
    resources = Resources({"in_storage":in_storage})
    gcs = GridcellSet(resources)
    gcs.load_dataset(resources=resources, attributes=SetAttribute.ALL)

    def testMatplotlibEngine(self):
        dv = DataSetVisualization(dataset=self.gcs, display_attribute="residential_units", engine_name="matplotlib")
        dv.display()

    def testOpenEVEngine(self):
        dv = DataSetVisualization(dataset=self.gcs, display_attribute="residential_units", engine_name="OpenEV")
        dv.display()

    def testThubanEngine(self):
        dv = DataSetVisualization(dataset=self.gcs, display_attribute="residential_units", engine_name="Thuban")
        dv.display()

    def testFloatCanvasEngine(self):
        dv = DataSetVisualization(dataset=self.gcs, display_attribute="residential_units", engine_name="FloatCanvas")
        dv.display()
        
if __name__ == "__main__":
    unittest.main()
