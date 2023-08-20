import logging
import logging.config
import os
from datetime import datetime
from os.path import abspath, dirname, join

import __main__
import yaml


def initialize_logger(logger_name, log_config_file, logger='root', log_level="INFO"):
    base_dir = abspath(dirname(str(__main__.__file__ )))
    logs_dir = base_dir + str("/.logs")
    os.makedirs(logs_dir, exist_ok=True)
    logs_target = join(logs_dir, f"{logger_name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
    logging.Formatter.default_msec_format = '%s.%03d'
            
    with open(log_config_file,  "r", encoding="utf8") as f:
        yaml_config = yaml.safe_load(f.read())
        yaml_config["handlers"]["file"]["filename"] = logs_target
        logging.config.dictConfig(yaml_config)
    
    logger = logging.getLogger(logger)
    logger.setLevel(getattr(logging, log_level))
    
    return logger