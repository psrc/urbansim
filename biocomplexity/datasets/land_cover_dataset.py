# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset
from numpy import indices, logical_not, where, logical_or
from numpy import ma
import os

class LandCoverDataset(UrbansimDataset):
    """Set of land covers."""

    id_name_default = []
    in_table_name_default = "land_covers"
    out_table_name_default = "land_covers_exported"
    dataset_name = "land_cover"
    nodata_value_default = -9999
    missingdata_value_default = 0
    partition_name = "partition"
    _coordinate_system = ('relative_x', 'relative_y')
    
    def __init__(self, *args, **kwargs):
        UrbansimDataset.__init__(self, *args, **kwargs)
        # get header of the first attribute
        for name in [self.partition_name, self._id_names]:
            try:
                self.header = self.get_attribute_header(name)
            except:
                self.header = None    
            if self.header and ("relative_x" not in self.get_primary_attribute_names()):
                # add x and y
                xy2d = indices((int(self.header["nrows"]), int(self.header["ncols"])))
                x = xy2d[0].ravel()
                y = xy2d[1].ravel()
                self.add_attribute(name="relative_x", data=x)
                self.add_attribute(name="relative_y", data=y)
                break
        self.mask = None
        
    def get_2d_attribute(self, attribute):
        return UrbansimDataset.get_2d_attribute(self, attribute=attribute)
    
    def flatten_by_id(self, two_d_array):
        return UrbansimDataset.flatten_by_id(self, two_d_array)
            
    def get_mask(self, is_2d_version = False):
        """Return an array with 1's where data has NOVALUE, otherwise 0.
        If is_2d_version return 2d array"""
        
        # find attr that is not an id or x or y
        attr_name = None
        for attr in [self.partition_name] + self.get_primary_attribute_names():
            if attr not in self.get_id_name()+["relative_x", "relative_y"] \
                   and attr in self.get_primary_attribute_names():
                attr_name = attr
                break
        return self.get_mask_of_attribute(attr_name, is_2d_version)    

    
    def true_size(self):
        """Return size of the dataset where NODATA are not counted."""
        if self.mask is None:
            self.mask = self.get_mask()
        unmask = logical_not(self.mask)
        return unmask.sum()
        
    def get_mask_of_attribute(self, attribute, is_2d_version = False):
        """Get mask for lct."""
        
        if attribute is None:
            raise StandardError, "No non-attributes found. Cannot create mask."
         
        if is_2d_version:
            values =self.get_2d_attribute(attribute)    
        else:
            values =self.get_attribute(attribute)

        nodata_val = self.get_nodata_value()
        missingdata_val = self.get_missing_data_value()
        self.resources["NODATA_value"] = nodata_val
        self.resources["MISSING_value"] = missingdata_val

        values = ma.filled(values, nodata_val)
        nodata_filter = where(values == nodata_val, True, False)
        
        return logical_or(where(values == missingdata_val, True, False), nodata_filter)
        
    def get_nodata_value(self):
        try:
            nodata_val = int(self.header["NODATA_value"])
        except:
            nodata_val = self.nodata_value_default
        return nodata_val
            
    def get_missing_data_value(self):
        try:
            missingdata_val = int(self.header["MISSING_value"])
        except:
            missingdata_val = self.missingdata_value_default
        return missingdata_val