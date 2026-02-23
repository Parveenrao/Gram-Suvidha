import logging
import os 
from logging.handlers import RotatingFileHandler   # auto rotates log files when size limits

os.makedirs("logs" , exist_ok=True)                # create log folder if not exist , no error if already exist


def get_logger(name : str) -> logging.Logger:
    logger = logging.getLogger(name)          # creates or gets existing logger with that name
    logger.setLevel(logging.DEBUG)            # logger will capture DEBUG and above debug (DEBUG , INFO , WARNING , ERROR , CRITICAl)
    
    
    console_handler = logging.StreamHandler()  # Print logs to the terminal
    console_handler.setLevel(logging.INFO)     # terimal shows info and above only
    
    
    file_handler = RotatingFileHandler(
    "logs/app.log",                            # log file path
    maxBytes=5 * 1024 * 1024,                  # rotate when file hits 5MB
    backupCount=3                              # keeps last 3 old files: app.log.1, app.log.2, app.log.3
    )
    
    file_handler.setLevel(logging.DEBUG)       # file saves everything including DEBUG
    
    formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
     )
                            #  output looks like:
                            # 2024-01-15 10:30:45 | INFO | app.routers.auth | Login successful | phone=9876543210
    
    console_handler.setFormatter(formatter)    # apply format to console
    file_handler.setFormatter(formatter)       # apply format to file

    if not logger.handlers:                    # prevent adding duplicate handlers
        logger.addHandler(console_handler)     # attach console handler to logger
        logger.addHandler(file_handler)        # attach file handler to logger
        
    return logger  # return ready-to-use logger    

