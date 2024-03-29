# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

# open a traits-based GUI for editing PSRC indicator requests

from opus_core.indicator_framework.traits.traits_indicator_handler import TraitsIndicatorHandler

handler = TraitsIndicatorHandler()
handler.open_editor(package_order = ['sanfrancisco','urbansim','opus_core'])