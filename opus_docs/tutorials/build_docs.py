# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os
import opus_docs.tools

def main():
    opus_docs.tools.build(["run-eugene-model", "lorenz-curve"],
                          os.path.join(opus_docs.__path__[0], "tutorials"))

if __name__ == "__main__":
    main()
