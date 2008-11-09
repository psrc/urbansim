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

import os
import opus_docs.tools

def main():
    path = os.path.join(opus_docs.__path__[0], "tutorials")
    modules = ["run-eugene-model", "lorenz-curve"]
    opus_docs.tools.build(modules, cwd=path, make_bibliography_and_index=False)

if __name__ == "__main__":
    main()
