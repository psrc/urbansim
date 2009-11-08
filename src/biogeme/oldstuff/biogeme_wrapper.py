#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

from biogeme.biogeme_coefficient import CoefficientEstimate

class BiogemeOutputFile(object):
    """Reads biogeme output files"""
    
    def __init__(self, file_name):
        """file_name: path to the biogeme output file to be read"""
        self.coefficients = {}
        
        output = file(file_name)
        lines = output.readlines()
        # find the start and end indices of the lines we want
        start = lines.index([x for x in lines if x.startswith("Utility parameters")][0]) + 3
        end = lines.index([x for x in lines if x.startswith("Scale parameters")][0])
        # create a CoefficientEstimate object for each of the lines
        for line in lines[start:end]:
            fields = line.split()
            # line format is: Name Value Stderr t-test RobustStderr Robust-t-test
            self.coefficients[fields[0]] = CoefficientEstimate(name=fields[0],\
                value=fields[1], stderr=fields[2], t_test=fields[3])
                
    def get_estimate(self, coeff_name):
        """coeff_name: the name of the coefficient to get the estimate for,
        as given to biogeme"""
        return self.coefficients[coeff_name]
        