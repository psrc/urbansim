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


try: 
    from sqlalchemy.databases import postgres
    
    class PGCascadeSchemaDropper(postgres.PGSchemaDropper):
        def visit_table(self, table):
            for column in table.columns:
                if column.default is not None:
                    self.traverse_single(column.default)
            self.append("\nDROP TABLE " +
                        self.preparer.format_table(table) +
                        " CASCADE")
            self.execute()
    
    postgres.dialect.schemadropper = PGCascadeSchemaDropper

except:
    pass