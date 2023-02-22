import csv
import os
import sys
from com.config import Config
from com.log import Logger
import logging

config = Config()
log = Logger(__name__, CmdLevel=logging.INFO, FileLevel=logging.INFO)


class Csvparser(object):

    def __init__(self, path):
        # get current directory
        path_current_directory = os.path.dirname(__file__)
        csv_file_path = os.path.join(path_current_directory, path)
        print(csv_file_path)
        self.csv_file_path = csv_file_path

        if os.path.exists(csv_file_path):
            print('OK')
            try:
                log.logger.info('reading apis from csv file: "{}"'.format(csv_file_path))
                with open(csv_file_path, 'r', encoding='utf8') as f:
                    rows_temp = csv.DictReader(f)
                    if not rows_temp:
                        log.logger.info('No content in csv file: "{}"!!!'.format(csv_file_path))
                        sys.exit()
                    else:
                        li = []
                        for row in rows_temp:
                            li.append(row)
                        self.rows = li
                        log.logger.info('reading csv file: "{}" finished'.format(csv_file_path))
            except IOError as e:
                log.logger.log(logging.ERROR, 'cannot open csv file: "{}"!!!'.format(csv_file_path))
                raise e
        else:
            log.logger.log(logging.ERROR, 'csv file not exist, aborting!!!')
            sys.exit()
