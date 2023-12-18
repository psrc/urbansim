# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

# version 0.1
# Author: Jesse Ayers

# Requirements:
#   -Python 2.5.1, see www.python.org
#   -SQLAlchemy 0.4, see www.sqlalchemy.org
#   -Depending on which type of SQL DBMS you are using, you will also need
#    to install the appropriate database connector for Python
#    See http://www.sqlalchemy.org/docs/04/intro.html#overview_sqlalchemy_dbms


from sqlalchemy import *

class raw_pums_data_processor(object):
    def __init__(self,  
                 username, password, hostname, 
                 database_name, protocol, pums_file,
                 port=None):
        
        if port is not None:
            port_string = ':%s' % port
        else:
            port_string = ''
        
        connection_string = '%s://%s:%s@%s%s/%s' % (
            protocol,
            username,
            password,
            hostname,
            port_string,
            database_name
            )     
        
        self._engine = create_engine(connection_string)
        self._metadata = MetaData(
            bind = self._engine
        )
        
        # Set beginning and end indexes for parsing household records
        self.hh_beg = [0, 1, 8, 9, 11, 12, 13, 18, 23, 27, 31, 35, 39, 41, 43, 57, 71, 85, 99, 101, 105, 107, 108, 109, 110, 111, 112, 113, 114, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 145, 146, 150, 151, 155, 156, 160, 161, 165, 166, 167, 168, 169, 170, 175, 176, 177, 178, 183, 184, 185, 186, 188, 189, 190, 191, 195, 196, 200, 201, 203, 204, 205, 206, 211, 212, 213, 215, 217, 219, 221, 223, 224, 225, 226, 227, 232, 235, 236, 240, 243, 244, 245, 246, 247, 248, 250, 258]
        self.hh_end = [1, 8, 9, 11, 12, 13, 18, 23, 27, 31, 35, 39, 41, 43, 57, 71, 85, 99, 101, 105, 107, 108, 109, 110, 111, 112, 113, 114, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 145, 146, 150, 151, 155, 156, 160, 161, 165, 166, 167, 168, 169, 170, 175, 176, 177, 178, 183, 184, 185, 186, 188, 189, 190, 191, 195, 196, 200, 201, 203, 204, 205, 206, 211, 212, 213, 215, 217, 219, 221, 223, 224, 225, 226, 227, 232, 235, 236, 240, 243, 244, 245, 246, 247, 248, 250, 258, 266]
        # Set households table field names and lengths
        self.hh_field_names = ['RECTYPE', 'SERIALNO', 'SAMPLE', 'STATE', 'REGION', 'DIVISION', 'PUMA5', 'PUMA1', 'MSACMSA5', 'MSAPMSA5', 'MSACMSA1', 'MSAPMSA1', 'AREATYP5', 'AREATYP1', 'TOTPUMA5', 'LNDPUMA5', 'TOTPUMA1', 'LNDPUMA1', 'SUBSAMPL', 'HWEIGHT', 'PERSONS', 'UNITTYPE', 'HSUB', 'HAUG', 'VACSTAT', 'VACSTATA', 'TENURE', 'TENUREA', 'BLDGSZ', 'BLDGSZA', 'YRBUILT', 'YRBUILTA', 'YRMOVED', 'YRMOVEDA', 'ROOMS', 'ROOMSA', 'BEDRMS', 'BEDRMSA', 'CPLUMB', 'CPLUMBA', 'CKITCH', 'CKITCHA', 'PHONE', 'PHONEA', 'FUEL', 'FUELA', 'VEHICL', 'VEHICLA', 'BUSINES', 'BUSINESA', 'ACRES', 'ACRESA', 'AGSALES', 'AGSALESA', 'ELEC', 'ELECA', 'GAS', 'GASA', 'WATER', 'WATERA', 'OIL', 'OILA', 'RENT', 'RENTA', 'MEALS', 'MEALSA', 'MORTG1', 'MORTG1A', 'MRT1AMT', 'MRT1AMTA', 'MORTG2', 'MORTG2A', 'MRT2AMT', 'MRT2AMTA', 'TAXINCL', 'TAXINCLA', 'TAXAMT', 'TAXAMTA', 'INSINCL', 'INSINCLA', 'INSAMT', 'INSAMTA', 'CONDFEE', 'CONDFEEA', 'VALUE', 'VALUEA', 'MHLOAN', 'MHLOANA', 'MHCOST', 'MHCOSTA', 'HHT', 'P65', 'P18', 'NPF', 'NOC', 'NRC', 'PSF', 'PAOC', 'PARC', 'SVAL', 'SMOC', 'SMOCAPI', 'SRNT', 'GRENT', 'GRAPI', 'FNF', 'HHL', 'LNGI', 'WIF', 'EMPSTAT', 'WORKEXP', 'HINC', 'FINC']
        self.hh_field_lengths = [1, 7, 1, 2, 1, 1, 5, 5, 4, 4, 4, 4, 2, 2, 14, 14, 14, 14, 2, 4, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 1, 4, 1, 4, 1, 4, 1, 4, 1, 1, 1, 1, 1, 5, 1, 1, 1, 5, 1, 1, 1, 2, 1, 1, 1, 4, 1, 4, 1, 2, 1, 1, 1, 5, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 5, 3, 1, 4, 3, 1, 1, 1, 1, 1, 2, 8, 8]
        
        # Set beginning and end indexes for parsing person records
        self.pp_beg = [0, 1, 8, 10, 11, 12, 16, 18, 19, 20, 21, 22, 23, 24, 26, 27, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 40, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 54, 55, 55, 58, 58, 61, 62, 63, 64, 65, 65, 68, 69, 70, 71, 71, 74, 75, 76, 77, 81, 82, 83, 84, 84, 87, 88, 93, 98, 100, 102, 106, 110, 114, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 153, 154, 155, 156, 156, 159, 160, 165, 170, 172, 174, 178, 182, 186, 190, 192, 193, 194, 195, 198, 199, 202, 203, 204, 205, 206, 207, 208, 209, 210, 213, 214, 222, 222, 225, 226, 226, 233, 234, 235, 236, 237, 239, 240, 242, 243, 249, 250, 256, 257, 263, 264, 269, 270, 275, 276, 281, 282, 288, 289, 295, 296, 303, 304, 311, 314]
        self.pp_end = [1, 8, 10, 11, 12, 16, 18, 19, 20, 21, 22, 23, 24, 26, 27, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 40, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 54, 55, 58, 58, 61, 61, 62, 63, 64, 65, 68, 68, 69, 70, 71, 74, 74, 75, 76, 77, 81, 82, 83, 84, 87, 87, 88, 93, 98, 100, 102, 106, 110, 114, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 153, 154, 155, 156, 159, 159, 160, 165, 170, 172, 174, 178, 182, 186, 190, 192, 193, 194, 195, 198, 199, 202, 203, 204, 205, 206, 207, 208, 209, 210, 213, 214, 222, 225, 225, 226, 233, 233, 234, 235, 236, 237, 239, 240, 242, 243, 249, 250, 256, 257, 263, 264, 269, 270, 275, 276, 281, 282, 288, 289, 295, 296, 303, 304, 311, 314, 316]
        # Set persons table field names and lengths
        self.pp_field_names = ['RECTYPE', 'SERIALNO', 'PNUM', 'PAUG', 'DDP', 'PWEIGHT', 'RELATE', 'RELATEA', 'OC', 'RC', 'PAOCF', 'SEX', 'SEXA', 'AGE', 'AGEA', 'HISPAN', 'HISPANA', 'NUMRACE', 'WHITE', 'BLACK', 'AIAN', 'ASIAN', 'NHPI', 'OTHER', 'RACE1', 'RACE2', 'RACE3', 'RACEA', 'MARSTAT', 'MARSTATA', 'MSP', 'SFN', 'SFREL', 'ENROLL', 'ENROLLA', 'GRADE', 'GRADEA', 'EDUC', 'EDUCA', 'ANCFRST5', 'ANCFRST1', 'ANCSCND5', 'ANCSCND1', 'ANCA', 'ANCR', 'SPEAK', 'SPEAKA', 'LANG5', 'LANG1', 'LANGA', 'ENGABIL', 'ENGABILA', 'POB5', 'POB1', 'POBA', 'CITIZEN', 'CITIZENA', 'YR2US', 'YR2USA', 'MOB', 'MOBA', 'MIGST5', 'MIGST1', 'MIGSTA', 'MIGPUMA5', 'MIGPUMA1', 'MIGAREA5', 'MIGAREA1', 'MIGCMA5', 'MIGCMA1', 'MIGPMA5', 'MIGPMA1', 'SENSORY', 'SENSORYA', 'PHYSCL', 'PHYSCLA', 'MENTAL', 'MENTALA', 'SLFCARE', 'SLFCAREA', 'ABGO', 'ABGOA', 'ABWORK', 'ABWORKA', 'DISABLE', 'GRANDC', 'GRANDCA', 'RSPNSBL', 'RSPNSBLA', 'HOWLONG', 'HOWLONGA', 'MILTARY', 'MILTARYA', 'VPS1', 'VPS2', 'VPS3', 'VPS4', 'VPS5', 'VPS6', 'VPS7', 'VPS8', 'VPS9', 'VPSA', 'MILYRS', 'MILYRSA', 'VPSR', 'ESR', 'ESRA', 'ESP', 'POWST5', 'POWST1', 'POWSTA', 'POWPUMA5', 'POWPUMA1', 'POWAREA5', 'POWAREA1', 'POWCMA5', 'POWCMA1', 'POWPMA5', 'POWPMA1', 'TRVMNS', 'TRVMNSA', 'CARPOOL', 'CARPOOLA', 'LVTIME', 'LVTIMEA', 'TRVTIME', 'TRVTIMEA', 'LAYOFF', 'ABSENT', 'RECALL', 'LOOKWRK', 'BACKWRK', 'LASTWRK', 'LASTWRKA', 'INDCEN', 'INDCENA', 'INDNAICS', 'OCCCEN5', 'OCCCEN1', 'OCCCENA', 'OCCSOC5', 'OCCSOC1', 'CLWKR', 'CLWKRA', 'WRKLYR', 'WRKLYRA', 'WEEKS', 'WEEKSA', 'HOURS', 'HOURSA', 'INCWS', 'INCWSA', 'INCSE', 'INCSEA', 'INCINT', 'INCINTA', 'INCSS', 'INCSSA', 'INCSSI', 'INCSSIA', 'INCPA', 'INCPAA', 'INCRET', 'INCRETA', 'INCOTH', 'INCOTHA', 'INCTOT', 'INCTOTA', 'EARNS', 'POVERTY', 'FILLER']
        self.pp_field_lengths = [1, 7, 2, 1, 1, 4, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 3, 3, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 3, 3, 1, 1, 1, 4, 1, 1, 1, 3, 3, 1, 5, 5, 2, 2, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3, 3, 1, 5, 5, 2, 2, 4, 4, 4, 4, 2, 1, 1, 1, 3, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 8, 3, 3, 1, 7, 7, 1, 1, 1, 1, 2, 1, 2, 1, 6, 1, 6, 1, 6, 1, 5, 1, 5, 1, 5, 1, 6, 1, 6, 1, 7, 1, 7, 3, 2]
            
    def create_hh_table(self, pums_hh_table_name):
        # Create initial households table object
        pums_hh_table = Table(pums_hh_table_name, self._metadata, Column(self.hh_field_names[0], String(self.hh_field_lengths[0])))
        # Loop through remainder of fields and add them to the table
        x = 1
        for i in self.hh_field_names:
            if i == 'RECTYPE':
                pass
            else:
                col = Column(self.hh_field_names[x], String(self.hh_field_lengths[x]))
                pums_hh_table.append_column(col)
                x += 1
        # Create the households table in the database
        pums_hh_table.create()
    
    def create_pp_table(self, pums_pp_table_name):
        # Create inital persons table object
        pums_pp_table = Table(pums_pp_table_name, self._metadata, Column(self.pp_field_names[0], String(self.pp_field_lengths[0])))
        # Loop through remainder of fields and add them to the table
        x = 1
        for i in self.pp_field_names:
            if i == 'RECTYPE':
                pass
            else:
                col = Column(self.pp_field_names[x], String(self.pp_field_lengths[x]))
                pums_pp_table.append_column(col)
                x += 1
        # Create the persons table in the database
        pums_pp_table.create()
    
    def get_next_hh_record(self, open_pums_file):
        line = open_pums_file.readline()
        if line == None:
            return None
        else:
            while line:
                if line[0] == 'H':
                    return line
                    break
                else:
                    line = open_pums_file.readline()
    
    def get_next_hh_record_as_dict(self, open_pums_file):
        line = self.get_next_hh_record(open_pums_file = open_pums_file)
        if line == None:
            return None
        insrt = []
        indx = 0
        y = 0
        for i in self.hh_beg:
            x = line[self.hh_beg[y]:self.hh_end[y]]
            insrt.append(x)
            y += 1
        zipped = list(zip(self.hh_field_names, insrt))
        dic = dict(zipped)
        return dic
    
    def insert_hh_records(self, pums_hh_table_name, pums_file):
        f = open(pums_file)
        self._metadata.reflect()
        pums_hh_table = Table(pums_hh_table_name, self._metadata, autoload=True)
        record = self.get_next_hh_record_as_dict(open_pums_file = f)
        flush_after = 1000
        list_to_insert = []
        while(record):
            list_to_insert.append(record)
            if len(list_to_insert) > flush_after:
                pums_hh_table.insert().execute(list_to_insert)
                list_to_insert = []
            record = self.get_next_hh_record_as_dict(open_pums_file = f)
        pums_hh_table.insert().execute(list_to_insert)
    
    def get_next_pp_record(self, open_pums_file):
        line = open_pums_file.readline()
        if line == None:
            return None
        else:
            while line:
                if line[0] == 'P':
                    return line
                    break
                else:
                    line = open_pums_file.readline()
    
    def get_next_pp_record_as_dict(self, open_pums_file):
        line = self.get_next_pp_record(open_pums_file = open_pums_file)
        if line == None:
            return None
        insrt = []
        indx = 0
        y = 0
        for i in self.pp_beg:
            x = line[self.pp_beg[y]:self.pp_end[y]]
            insrt.append(x)
            y += 1
        zipped = list(zip(self.pp_field_names, insrt))
        dic = dict(zipped)
        return dic                
    
    def insert_pp_records(self, pums_pp_table_name, pums_file):
        f = open(pums_file)
        self._metadata.reflect()
        pums_pp_table = Table(pums_pp_table_name, self._metadata, autoload=True)
        record = self.get_next_pp_record_as_dict(open_pums_file = f)
        flush_after = 1000
        list_to_insert = []
        while(record):
            list_to_insert.append(record)
            if len(list_to_insert) > flush_after:
                pums_pp_table.insert().execute(list_to_insert)
                list_to_insert = []
            record = self.get_next_pp_record_as_dict(open_pums_file = f)
        pums_pp_table.insert().execute(list_to_insert)
