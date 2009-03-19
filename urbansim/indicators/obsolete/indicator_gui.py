# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

# open a traits-based GUI for editing PSRC indicator requests

from opus_core.indicator_framework.traits.traits_indicator_handler \
    import TraitsIndicatorHandler

handler = TraitsIndicatorHandler()
handler.open_editor(package_order = ['urbansim','opus_core'])

