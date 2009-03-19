# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

raise "Please chance the name of the package in tests.all_tests" #remove this line after changing the package name

from opus_core.tests.utils.package_tester import PackageTester

PackageTester().run_all_tests_for_package('z_template_project') 