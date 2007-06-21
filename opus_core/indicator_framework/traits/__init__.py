#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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

try:
    from opus_core.indicator_framework.traits.traits_source_data import TraitsSourceData
    from opus_core.indicator_framework.traits.traits_abstract_indicator import TraitsAbstractIndicator
    from opus_core.indicator_framework.traits.traits_indicator_handler import TraitsIndicatorHandler
except:
    from opus_core.logger import logger
    logger.log_warning('Could not load traits.ui. Skipping %s!' % __file__)
