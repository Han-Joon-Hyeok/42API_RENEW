import os
import logging

import env

log_file_path = "{}/{}".format(env.config["LOG_FILE_DIRECTORY"], env.config["LOG_FILE_NAME"])

def create_log_file():

    if not os.path.exists(env.config["LOG_FILE_DIRECTORY"]):
        os.makedirs(env.config["LOG_FILE_DIRECTORY"])
    
    if not os.path.exists(log_file_path):
        with open(log_file_path, "w") as f:
            f.write("")

def setup_logger():
    create_log_file()
    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,
        format='[%(levelname)s] %(asctime)s - %(filename)s, line %(lineno)d, in %(funcName)s\n  %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )