import os
import logging
from logging.handlers import TimedRotatingFileHandler

###################################################### CONFIG EXTRACTION ###################################################
class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def file_read():
    config_file_path = os.environ.get("config_file_path")
    
    if config_file_path is not None:
        dir_path = config_file_path
    else:
        dir_path = os.path.dirname(os.path.abspath(__file__))   
         
    temp_dict = {}
    con_file = os.path.join(dir_path, 'config.properties')
    if os.path.isfile(con_file):
        with open(con_file, "r") as cur_file:
            for line in cur_file: 
                line = line.rstrip()
                if "=" not in line: continue  # skips blanks and comments
                if line.startswith("#"): continue  # skips comments which contain #
                k, v = line.split("=", 1)
                temp_dict[k.strip()] = v.strip()
    else:
        raise FileNotFoundError("!!!!! config.properties file is not present !!!!!")
    return temp_dict

    
CONSTS = AttributeDict(file_read())

###################################################### LOGGING CONFIGURATION #################################################
logging.basicConfig(level=CONSTS.log_level,
                    handlers=[TimedRotatingFileHandler(filename=CONSTS.log_file_path,
                                                       when=CONSTS.file_rotation,
                                                       backupCount=int(CONSTS.backup_count))],
                    format=CONSTS.log_format)
##############################################################################################################################
