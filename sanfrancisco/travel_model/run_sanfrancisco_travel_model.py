# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2010 University of Washington and the SFCTA
# See opus_core/LICENSE 


from opus_core.store.flt_storage import flt_storage
from opus_core.resources import Resources
from numpy import array, float32, ones
from os.path import join
from dbfpy import dbf
import csv, os, re, shutil, subprocess, sys
from opus_core.logger import logger
from travel_model.models.run_travel_model import RunTravelModel
from opus_core.misc import module_path_from_opus_path
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration

class RunSanfranciscoTravelModel(RunTravelModel):
    """Run the travel model.
    """
    SUBDIR_TAZ_DATA_PROCESSOR       = "TazDataProcessor"
    SUBDIR_POPULATION_SYNTHESIZER   = "PopSyn"
    SUBDIR_LANDUSE_INPUTS           = "LandUseInputs"
    RUN_DISPATCH                    = "runmodel.jset"
    DISPATCH                        = r"Y:\champ\util\bin\dispatch.bat"
    CLUSTER_MACHINE                 = "taraval"

    def run(self, myconfig={}, year=2001):
        """Runs the travel model, using appropriate info from config. 
        """
        tm_config   = myconfig["travel_model_configuration"]
        
        # verify that the base directory exists and there's a runbatch in it, or we're a nogo
        base_dir    = tm_config['travel_model_base_directory']    
        if not os.path.exists(base_dir):
            raise StandardError, \
                "Travel model base directory '%s' must exist with standard %s" % (base_dir, tm_config[year]["RUNBATCH"])
                 
        src_runmodelfile = os.path.join(base_dir, tm_config[year]["RUNBATCH"])
        if not os.path.exists(src_runmodelfile):
            raise StandardError, \
                "Travel model base directory '%s' must exist with a standard %s" % (base_dir, tm_config[year]["RUNBATCH"])            
        
        run_dir     = os.path.join(base_dir, tm_config[year]['year_dir'])
        if not os.path.exists(run_dir):
            os.makedirs(run_dir)
        
        # if the final skims are already there, then abort -- this has run already
        if os.path.exists(os.path.join(run_dir, "finalTRNWLWAM.h5")):
            logger.log_status("Final skims found in %s, skipping travel model" % run_dir)
            return
        
        runinputs_dir = os.path.join(run_dir, self.SUBDIR_LANDUSE_INPUTS)
        if not os.path.exists(runinputs_dir):
            os.makedirs(runinputs_dir)
        
        # run the TAZ data processor and the Population Synthesizers
        self._run_TazDataProcessor(tm_config, year, run_dir)
        self._run_PopSyn(tm_config, year, run_dir)
        
        config_regexlist = [ \
          [r"(set LANDUSE=)(\S*)",    r"\1.\%s" % (self.SUBDIR_LANDUSE_INPUTS)],
        ]
        
        print tm_config[year]
        # if these are specified in the config use them
        for varname in ["BASEDEMAND", "MTCDEMAND", "NETWORKS"]:
            if varname in tm_config[year]:
                config_regexlist.append([r"(?P<set>set %s=)\S*[ ]*$" % varname, 
                                         r"\g<set>"+tm_config[year][varname].replace('\\','\\\\')])
        
        # but these remain the default... just using the one in the file and subbing the year
        config_regexlist.append([r"(?P<set>set (BASEDEMAND|MTCDEMAND|NETWORKS)=\S*)(\d\d\d\d)[ ]*$", r"\g<set>" + str(year)])
        logger.log_status("config_regexlist=" + str(config_regexlist))

        # make the run
        shutil.copy2(src_runmodelfile, run_dir)
        self._updateConfigPaths( os.path.join(run_dir, tm_config[year]["RUNBATCH"]), config_regexlist, 
                                 doubleBackslash=False)
        
        # dispatcher to taraval, where models start
        outfile = open( os.path.join(run_dir, self.RUN_DISPATCH), 'w')
        outfile.write("%s\n" % (tm_config[year]["RUNBATCH"]))
        outfile.close()
        
        # run it!
        cmd         = self.DISPATCH + " " + self.RUN_DISPATCH + " " + self.CLUSTER_MACHINE
        logger.start_block("Running TRAVEL MODDEL [%s]" % (cmd))
        tmproc = subprocess.Popen( cmd, cwd = run_dir, stdout=subprocess.PIPE ) 
        for line in tmproc.stdout:
            logger.log_status(line.strip('\r\n'))
        tmret  = tmproc.wait()
        logger.log_status("Returned %d" % (tmret))
        # TODO - why does it return 1 when it seems ok?!?!
        if tmret != 0 and tmret != 1: raise StandardError, "%s exited with bad return code" % (cmd)
        logger.end_block()

    def _run_TazDataProcessor(self, tm_config, year, run_dir):
        """ Gets the inputs all setup and then runs the TazDataProcessor.
        """
        # update sfzones.csv with the landusemodel output
        dest_dir = os.path.join(run_dir, self.SUBDIR_TAZ_DATA_PROCESSOR)
        if not os.path.exists(dest_dir): os.makedirs(dest_dir)
            
        # create inputs directory, if needed
        dest_inputdir = os.path.join(dest_dir, "input")
        if not os.path.exists(dest_inputdir): os.makedirs(dest_inputdir)

        # copy over data files from the source data directory
        sfzonesfile         = "sfzones%d.csv" % (year)
        tazkeyfile          = "TazKey.csv"
        shutil.copy2(os.path.join(tm_config['tazdataprocessor_datadir'], sfzonesfile),  dest_inputdir)
        shutil.copy2(os.path.join(tm_config['tazdataprocessor_srcdir'],"input","TazKey_UrbanSim.csv"), 
                     os.path.join(dest_inputdir,tazkeyfile))
        
        # copy over controls files
        dest_controlsdir = os.path.join(dest_dir, "controls")
        if os.path.exists(dest_controlsdir): shutil.rmtree(dest_controlsdir)
        
        src_controlsdir = os.path.join(tm_config['tazdataprocessor_srcdir'], "controls")
        shutil.copytree(src_controlsdir, dest_controlsdir)
        
        # update the controls file
        zmastfile           = "zmast%02d.dat" % (year % 100)
        azlosfile           = "azlos%02d.dat" % (year % 100)
        enrollfile          = "hbschool.zenroll.%d.dat" % (year)
        baseyearfile        = "baseyear.csv"
        
        controlsfile = os.path.join(dest_controlsdir,"tazdata.properties")
        logger.log_status("Updating TazDataProcessor Control file %s" % (controlsfile))
        self._updateConfigPaths(controlsfile, 
         [ [r"(tazkey\s*=\s*)(\S*)",   r"\1input\%s" % tazkeyfile ],
           [r"(sfzones\s*=\s*)(\S*)",  r"\1input\%s" % sfzonesfile],
           [r"(zmast\s*=\s*)(\S*)",    r"\1"+os.path.join(tm_config['tazdataprocessor_datadir'],zmastfile)],
           [r"(azlos\s*=\s*)(\S*)",    r"\1"+os.path.join(tm_config['tazdataprocessor_datadir'],azlosfile)],
           [r"(enroll\s*=\s*)(\S*)",   r"\1"+os.path.join(tm_config['tazdataprocessor_datadir'],enrollfile)],
           [r"(baseyear\s*=\s*)(\S*)", r"\1"+os.path.join(tm_config['tazdataprocessor_srcdir'],"input",baseyearfile)]
         ])
        
        # update the sfzones file
        shutil.move(os.path.join(dest_inputdir,sfzonesfile), os.path.join(dest_inputdir,sfzonesfile+".bak"))
        self._replaceCsvItems(os.path.join(dest_inputdir,sfzonesfile+".bak"),
                              os.path.join(run_dir,tm_config['urbansim_to_tm_variable_file']),
                              os.path.join(dest_inputdir,sfzonesfile), "SFTAZ")
        
        # copy over the batch              
        batfile             = "ProcessTazData.bat"
        shutil.copy2(os.path.join(tm_config['tazdataprocessor_srcdir'], batfile), dest_dir)
        
        # run the TazDataProcessor
        cmd         = os.path.join(dest_dir, batfile)
        logger.start_block("Running [%s]" % (cmd))
        tazdataproc = subprocess.Popen( cmd, cwd = dest_dir, stdout=subprocess.PIPE ) 
        for line in tazdataproc.stdout:
            logger.log_status(line.strip('\r\n'))
        tazdataret  = tazdataproc.wait()
        logger.log_status("Returned %d" % (tazdataret))
        if tazdataret != 0: raise StandardError,"TazDataProcessor exited with bad return code"
        logger.end_block()
        
        # clean the Allocate_nhb.csv file.  This should really be fixed in the TazDataProcessor
        self._clean_allocate_nhb(os.path.join(dest_dir, "Allocate_nhb.csv"))
        # postprocess the tazdata.dbf.  This should be done more cleanly also
        self._postprocessTazdata(os.path.join(dest_dir, "tazdata.dbf"),
                                 os.path.join(tm_config['tazdataprocessor_srcdir'], "tazdataAppend_UrbanSim.dbf"),
                                 os.path.join(dest_dir, "tazdata.dat"))
        
        # put the output files in place
        outputfiles = ["tazdata.dbf", 
                       "tazdata.dat",
                       "Allocate_nhb.csv",
                       "MTC_disaggregation.csv",
                       "MTC_disaggregation_hbw.csv",
                       "MTC_disaggregation_nhb.csv"
                      ]
        for outputfile in outputfiles:
            shutil.copy2(os.path.join(dest_dir, outputfile), 
                         os.path.join(run_dir, self.SUBDIR_LANDUSE_INPUTS))

    def _clean_allocate_nhb(self, src_csv):
        """ Workaround for TazDataProcessor bug that writes "NaN" entries when there was 0 population.
            Splits the MTAZ (non-existent) employment evenly in that case.
        """
        shutil.move(src_csv, src_csv+".bak")
        infile      = open(src_csv+".bak", 'rU')
        outfile     = open(src_csv, 'w')
        
        reader      = csv.reader(infile)
        writer      = csv.writer(outfile,lineterminator='\n')
        mtaz        = []
        sftaz       = []
        pct1        = []
        pct2        = []
        
        # read the entire input file
        for row in reader:
            mtaz.append(row[0])
            sftaz.append(row[1])
            pct1.append(row[2])
            pct2.append(row[3])
        N=len(mtaz)
        
        # look for NaN entries
        for i in range(N):
            if pct1[i]=='NaN':
                # find the other entries for this mtaz
                idx = []
                for j in range(N):
                    if mtaz[j]==mtaz[i]:
                        idx.append(j)
                L=len(idx)
                
                # set the percents to divvy it up       
                for k in idx:
                    pct1[k]=100.0/L
                    pct2[k]=100.0/L
                    #print k, pct1[k]
        
        for i in range(N):
            writer.writerow([mtaz[i],sftaz[i],pct1[i],pct2[i]])
        
        infile.close()
        outfile.close()        

    def _postprocessTazdata(self, src_dbf_file, append_dbf_file, dat_file):
        """ This hurts, it really does.  But group quarters needed to come from the zmast file, and
            HHPOP came from sfzones, and the TazDataProcessory couldn't handle combining those to
            make the total POP so we have to do so here.  Some day I hope this is cleaner -- maybe
            if group quarters population came out of UrbanSim, or the TazDataProcessor were a bit
            smarter...
        """
        shutil.move(src_dbf_file, src_dbf_file+".bak")
        dbfin       = dbf.Dbf(src_dbf_file+".bak", readOnly=1, ignoreErrors=True)
        dbfin2      = dbf.Dbf(append_dbf_file, readOnly=1)
        if len(dbfin) != len(dbfin2):
            raise StandardError, "%s and %s have different number of records" % (src_dbf_file, append_dbf_file)
       
        # read the append dbf file
        dist22 = {}
        dist40 = {}
        for rec in dbfin2:
            dist22[rec["SFTAZ"]] = rec["DIST22"]
            dist40[rec["SFTAZ"]] = rec["DIST40"]
        dbfin2.close()
        
        # add the two new fields
        dbfout      = dbf.Dbf(src_dbf_file, new=True)
        datout      = open(dat_file, 'w')
        fields      = []        
        for field in dbfin.fieldDefs:            
            if field.name == "DIST51":
                dbfout.addField(("DIST22", field.typeCode, field.length, field.decimalCount))
                dbfout.addField(("DIST40", field.typeCode, field.length, field.decimalCount))
                fields.append("DIST22")
                fields.append("DIST40")
            dbfout.addField((field.name, field.typeCode, field.length, field.decimalCount))
            fields.append(field.name)
        
        # update the dbf
        for rec in dbfin:
                        
            newrec  = dbfout.newRecord()
            for field in fields:
                if field=="POP":
                    newrec[field] = rec["GQPOP"] + rec["HHPOP"]
                elif field=="DIST22":
                    newrec[field] = dist22[rec["SFTAZ"]]
                elif field=="DIST40":
                    newrec[field] = dist40[rec["SFTAZ"]]
                else:
                    newrec[field] = rec[field]
                if field != fields[0]:
                    datout.write(" ")
                datout.write(str(newrec[field]))
            newrec.store()
            datout.write("\n")
        dbfout.close()
        datout.close()
        dbfin.close()

    def _replaceCsvItems(self, src_csv, overwrite_csv, dest_csv, indexcolname):
        """ Opens the src_csv, overwrites columns/data using the overwrite_csv, and writes the result into
            the dest_csv.  If this is useful, move to a standalone python file?
        """

        # read the overwrite file
        overwrite_colnameTocolnum   = {}  # map { "SFTAZ":0, "HHLDS":1, ...}
        overwrite_lines             = {}  # map indexval (e.g. SFTAZ) => [ val1, val2, val3, ...]
        
        overwritefile               = open(overwrite_csv, 'rU')
        line = overwritefile.readline()
        overwrite_columns           = line.strip().split(",")
        for i in range(len(overwrite_columns)):
            overwrite_colnameTocolnum[overwrite_columns[i]] = i
        for line in overwritefile:
            cols = line.strip().split(",")
            indexval = int(cols[overwrite_colnameTocolnum[indexcolname]])
            overwrite_lines[indexval] = cols
        overwritefile.close()
        
        # do the replacement
        infile          = open(src_csv, 'rU')
        outfile         = open(dest_csv, 'w')
        line            = infile.readline()
        outfile.write(line.strip())
        src_columns     = line.strip().split(",")
        try:
            indexcolnum     = src_columns.index(indexcolname)
            popcolnum       = src_columns.index("POP")
        except:
            logger.log_error("Column named %s not found in %s" % (indexcolname, src_csv))
            raise StandardError, "Column named %s not found in %s" % (indexcolname, src_csv)
        
        #try:
        #    popcolnum       = src_columns.index("POP")
        #    gqpopcolnum     = src_columns.index("GQPOP")
        #    hhpopcolnum     = src_columns.index("HHPOP")
        #except:
        #    logger.log_error("Column named POP,GQPOP or HHPOP not found in %s" % (src_csv))
        #    raise StandardError, "Column named POP,GQPOP or HHPOP not found in %s" % (src_csv)

        overwrite_colset    = []
        new_colset          = []
        for colname in overwrite_columns:
            if colname in src_columns:
                overwrite_colset.append(colname)
            else:
                new_colset.append(colname)
                outfile.write(",")
                outfile.write(colname)
        outfile.write("\n")
        
        logger.log_status("Overwriting columns %s from %s into %s" % 
                          (str(overwrite_colset), overwrite_csv, dest_csv))
        logger.log_status("Adding new columns %s" % (str(new_colset)))

        for line in infile:
            cols        = line.strip().split(",")
            indexval    = int(cols[indexcolnum])
            if indexval not in overwrite_lines:
                outfile.write(line.strip())
                # add the new columns
                for colname in new_colset:
                    outfile.write(",0")
                outfile.write("\n")
                continue
            
            # do the replacements
            for colnum in range(len(src_columns)):
                colname = src_columns[colnum]
                if colname in overwrite_colnameTocolnum:
                    cols[colnum] = overwrite_lines[indexval][overwrite_colnameTocolnum[colname]]
            
            # add the new columns
            for colname in new_colset:
                cols.append(overwrite_lines[indexval][overwrite_colnameTocolnum[colname]])
            
            # alas, this isn't generic
            # replace POP with HHPOP + GQPOP
            # cols[popcolnum] = cols[gqcolnum] + cols[hhpopcolnum]
            
            outfile.write(",".join(cols) + "\n")
        infile.close()
        outfile.close()

    def _run_PopSyn(self, tm_config, year, run_dir):
        """ Gets the inputs all setup and then runs the Population Synthesizer.
        """
        # update sfzones.csv with the landusemodel output
        dest_dir = os.path.join(run_dir, self.SUBDIR_POPULATION_SYNTHESIZER)
        if not os.path.exists(dest_dir): os.makedirs(dest_dir)
        
        # copy over inputs files
        dest_inputsdir = os.path.join(dest_dir, "inputs")
        if not os.path.exists(dest_inputsdir): os.makedirs(dest_inputsdir)        
        # copy over the tazdata from the TazDataProcessor step
        shutil.copy2(os.path.join(run_dir, self.SUBDIR_TAZ_DATA_PROCESSOR, "tazdata.dbf"), dest_inputsdir)
        
        # copy over controls files
        dest_controlsdir = os.path.join(dest_dir, "controls")
        if os.path.exists(dest_controlsdir): shutil.rmtree(dest_controlsdir)  
        src_controlsdir = os.path.join(tm_config['popsyn_srcdir'], "controls")
        shutil.copytree(src_controlsdir, dest_controlsdir)

        self._updateConfigPaths(os.path.join(dest_controlsdir, "hhSubmodels.properties"), 
         [ [r"(tazdata.file\s*=\s*)(\S*)",      r"\1inputs\tazdata.dbf"],
           [r"(tazdata.out.file\s*=\s*)(\S*)",  r"\1inputs\tazdata_converted.csv"],
           [r"(\S\s*=\s*)(inputs/)(\S*)",       "%s%s%s" % (r"\1",os.path.join(tm_config['popsyn_srcdir'],"inputs"),r"\\\3")]
         ])
        self._updateConfigPaths(os.path.join(dest_controlsdir, "arc.properties"), 
         [ [r"(Forecast.TazFile\s*=\s*)(\S*)",  r"\1inputs\tazdata_converted.csv"],
           [r"(\S\s*=\s*)(./inputs/)(\S*)",       "%s%s%s" % (r"\1",os.path.join(tm_config['popsyn_srcdir'],"inputs"),r"\\\3")]
         ])
        
        # make the outputs directory
        dest_outputsdir = os.path.join(dest_dir, "outputs")
        if not os.path.exists(dest_outputsdir): os.makedirs(dest_outputsdir)
        for dir in ["intermediate", "syntheticPop", "validation"]:
            newdir = os.path.join(dest_outputsdir, dir)
            if not os.path.exists(newdir): os.makedirs(newdir)

        # copy over the batch              
        batfile             = "runPopSyn.bat"
        shutil.copy2(os.path.join(tm_config['popsyn_srcdir'], batfile), dest_dir)
        
        # run the Population Synthesizer
        sfsampfile = os.path.join(dest_outputsdir, "syntheticPop", "sfsamp.txt")
        if os.path.exists(sfsampfile):
            logger.log_status("Synthesized population file %s exists -- skipping creation!" % sfsampfile)
        else:
            cmd         = os.path.join(dest_dir, batfile)
            logger.start_block("Running [%s]" % (cmd))
            popsynproc = subprocess.Popen( cmd, cwd = dest_dir, stdout=subprocess.PIPE ) 
            for line in popsynproc.stdout:
                logger.log_status(line.strip('\r\n'))
            popsynret  = popsynproc.wait()
            logger.log_status("Returned %d" % (popsynret))
            if popsynret != 0: raise StandardError, "Population Synthesizer exited with bad return code"

        # put the output files in place
        shutil.copy2(sfsampfile, os.path.join(run_dir, self.SUBDIR_LANDUSE_INPUTS))

        logger.end_block()
        


    def _updateConfigPaths(self, configfile, regexlist, doubleBackslash=True):
        """ Updates the given configfile with the given regex dictionary.
            Regexdict will is a list of tuples: [regex_str,replacement_str]; first match wins
        """
        slash_re = re.compile(r"([^\\])\\([^\\])")
        
        # make it a triple: [ regex_str, replacement_str, compiled regex ]
        for i in range(len(regexlist)):          
            regexlist[i].append(re.compile(regexlist[i][0],re.IGNORECASE))
            # and make the backslashes double
            if doubleBackslash: regexlist[i][1] = slash_re.sub(r"\1\\\\\2", regexlist[i][1])

        shutil.move(configfile, configfile+".bak")
        infile      = open(configfile+".bak", 'rU')
        outfile     = open(configfile, 'w')
        for line in infile:
            modified = False
            for i in range(len(regexlist)):
                (modline, n) = regexlist[i][2].subn(regexlist[i][1], line)
                if n > 0:
                    # forward slash to backslash
                    modline = modline.replace(r"/", r"\\")
                    # double the backslashes
                    if doubleBackslash: modline = slash_re.sub(r"\1\\\\\2", modline)
                    logger.log_status("Modified %s => %s in %s" % 
                                      (line.strip("\n\r"), modline.strip("\n\r"), configfile))
                    outfile.write(modline)
                    modified = True
                    break
            if not modified:
                outfile.write(line)

        infile.close()
        outfile.close()

if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    from optparse import OptionParser
    from opus_core.file_utilities import get_resources_from_file
    parser = OptionParser()
    parser.add_option("-r", "--resources", dest="resources_file_name", action="store", type="string",
                      help="Name of file containing resources")
    parser.add_option("-y", "--year", dest="year", action="store", type="int",
                      help="Year in which to 'run' the travel model")
    (options, args) = parser.parse_args()
    
    r = get_resources_from_file(options.resources_file_name)
    resources = Resources(get_resources_from_file(options.resources_file_name))

    SessionConfiguration(new_instance=True,
                         package_order=resources['dataset_pool_configuration'].package_order,                              
                         in_storage=AttributeCache())

    RunSanfranciscoTravelModel().run(resources, options.year)    
