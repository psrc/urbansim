#
# Opus software. Copyright (C) 1998-2007 University of Washington
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

from opus_core.datasets.dataset import Dataset
from StringIO import StringIO
from opus_core.variables.variable_name import VariableName
from scipy import ndimage

class GuiDataset(Dataset):
    """
    This class is specifically for methods called on dataset by the opus_gui
    """
    
    def summary(self, names=[], resources=None):
        """Print a summary of the attributes given in the list 'names'.
        If names is an empty list, display summary for all primary attributes
        plus all computed attributes.
        """
        if not names:
            names = self.get_attribute_names()
            for name in self.get_primary_attribute_names():
                if name not in names:
                    names.append(name)
            self.load_dataset_if_not_loaded(attributes=names)
        
        buffer = StringIO()
        buffer.write("%25s\t%8s\t%8s\t%9s\t%7s\t%7s" %("Attribute name", "mean", "sd", "sum", "min", "max"))
        buffer.write("\n%94s" % (94*("-")))
        
        if (not isinstance(names, list)) and (not isinstance(names, tuple)):
            names = [names]
        for item in names:
            item_name = VariableName(item)
            short_name = item_name.get_alias()
            if short_name not in self.get_id_name():
                if not (short_name in self.get_attribute_names()):
                    if short_name in self._primary_attribute_names:
                        self.load_dataset(attributes=[short_name])
                    else:
                        self.compute_variables([item], resources=resources)
                if self.get_data_type(item).char <> 'S':
                    s = self.attribute_sum(short_name)
                    values = self.get_attribute(short_name)
                    buffer.write("\n%25s\t%8s\t%8s\t%9g\t%7g\t%7g" %(short_name, round(values.mean(),2), round(ndimage.standard_deviation(values),2),
                                                                        s, values.min(), values.max()))

        size = "\n\nSize: %s records" % (str(self.size()))
        buffer.write(size)
        buffer.write("\nidentifiers: ")
        for idname in self.get_id_name():
            temp_string = "\t %s in range %s-%s" % (idname, self.get_attribute(idname).min(), self.get_attribute(idname).max())
            buffer.write(temp_string)
        
        return buffer