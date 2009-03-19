# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

import os
import opus_docs.tools

def main():
    opus_docs.tools.build(["opus-userguide"],
                          os.path.join(opus_docs.__path__[0], "manual"))

if __name__ == "__main__":
    main()
