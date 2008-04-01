import configure_path
import os, sys
from resources import Resources
from storage_creator import StorageCreator
from gridcellset.gridcells import GridcellSet


import Numeric as numpy
import numarray as na
import gdalnumeric
import gview
import gviewapp
import gtk

def convert_numarray_to_numeric_array(na_array):
    return numpy.array(na_array.tolist(), typecode=na_array.typecode())


#read in a dataset object as gdalnumeric

attribute_to_display = "residential_units"

dirEugene = os.environ['OPUSHOME'] + "/UrbanSim4/data/flt/Eugene_1980_baseyear"

storage_dictionary = Resources({"base":dirEugene})
in_storage = StorageCreator().get_storage("Flt", storage_dictionary)
resources = Resources({"in_storage":in_storage})
gcs = GridcellSet(resources)

twod_na_array_to_display = gcs.get_2d_attribute(attribute_to_display)

twod_numpy_array_to_display = convert_numarray_to_numeric_array(twod_na_array_to_display)
twod_numpy_array_to_display = numpy.transpose(twod_numpy_array_to_display)

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

imgds = gdalnumeric.OpenArray(twod_numpy_array_to_display)
imgraster = gview.GvRaster(dataset=imgds)
imgrlayer = gview.GvRasterLayer(raster=imgraster)

aview = gview.app.sel_manager.get_active_view()
aview.add_layer(imgrlayer)

gtk.mainloop()         # start the main event loop

