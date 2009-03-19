# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

import os

def get_project_year_dir(config, year):
    project_data_dir = config["directory"]   #C:/SEMCOG_baseline
    year_dir = config[year]  #'CoreEA05\\urbansim\\2001'
    dir_part1,dir_part2 = os.path.split(year_dir)
    while dir_part1:
        dir_part1, dir_part2 = os.path.split(dir_part1)
    project_year_dir = os.path.join(project_data_dir, dir_part2)   #C:/SEMCOG_baseline/CoreEA0511202006
    return project_year_dir

def set_project_ini_file(config, year):
    """ set project ini setting using values in config"""
    ini_file = config['project_ini']
    ini_fp = open(ini_file,"r")
    project_year_dir = get_project_year_dir(config, year)
    import ConfigParser
    cfg = ConfigParser.ConfigParser()
    cfg.readfp(ini_fp)
    for section in cfg.sections():
        for option in cfg.options(section):
            dir = cfg.get(section, option)  #[('c', '\semcog\semcog_bin.mode')]
            cfg.remove_option(section, option)
            
            file_name = os.path.basename(dir)
            if not os.path.splitext(file_name)[1]:   #special handling for data directory section
                file_name = ''
            new_dir = os.path.join(project_year_dir, file_name)
    #                new_option,new_value = new_dir.split(":")
            new_option = new_dir
            new_value = ''
            v=cfg.set(section, new_option, new_value)
    
       # cfg.write(ini_fp)
    
    #if '[UI File]' section is in ini file and config has key ui_file
    #overwrite [UI File] section with config['ui_file']
    #config['ui_file'] must be ui_file without extension
    ui_section = 'UI File'
    if cfg.has_section(ui_section):
        if 'ui_file' in config:
            ui_option = cfg.options(ui_section)[0]  #only 1 option
            ui_ext = os.path.splitext(ui_option)[1] #file extension
            cfg.remove_option(ui_section, ui_option)
            cfg.set(ui_section, config['ui_file'] + ui_ext, '')
            
    ini_fp.close()
    ini_fp = open(ini_file,"w")
    
    for section in cfg.sections():
        ini_fp.write("[%s]\n" % section)
        for option in cfg.options(section):
            ini_fp.write("%s\n" % option)
    
    ini_fp.close()
