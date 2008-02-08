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

class interp(object):
    def do_interp(self, first, last, steps):
        diff = last - first
        inc = diff/steps
        lst = []
        lst.append(first)
        for i in range(0,steps):
            x = lst[i] + inc
            lst.append(x)
        lst.pop()
        lst.append(last)
        return lst
            