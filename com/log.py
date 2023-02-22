import logging
import time
from com.config import Config
import os

config = Config()


class Logger(object):

    def __init__(self, logger, CmdLevel=logging.INFO, FileLevel=logging.INFO):
        """
        :param logger:
        :param CmdLevel:
        :param FileLevel:
        """
        try:
            self.logger = logging.getLogger(logger)
            self.logger.setLevel(logging.DEBUG)  # 设置日志输出的默认级别
            # log format 日志输出格式
            fmt = logging.Formatter('%(asctime)s - %(filename)s:[%(lineno)s] - [%(levelname)s] - %(message)s')
            # log file name 日志文件名称
            # self.LogFileName = os.path.join(conf.log_path, "{0}.log.txt".format(time.strftime("%Y-%m-%d")))# %H_%M_%S
            curr_time = time.strftime("%Y-%m-%d")
            # set file path 设置日志文件路径
            # get current directory
            path_current_directory = os.path.dirname(os.path.dirname(__file__))
            # get csv file path from config
            log_file_path_from_config = config.get_config('LOG', 'LOG_FILE_PATH')+ curr_time + '.txt'
            self.LogFileName = os.path.join(path_current_directory, log_file_path_from_config)

            #self.LogFileName = config.get_config('LOG', 'LOG_FILE_PATH') + curr_time + '.txt'
            #self.LogFileName = config.get_config('LOG', 'LOG_FILE_PATH_TEST')+curr_time+'.txt'

            # 设置控制台输出
            # sh = logging.StreamHandler()
            # sh.setFormatter(fmt)
            # sh.setLevel(CmdLevel)# 日志级别

            # file handler 设置文件输出
            fh = logging.FileHandler(self.LogFileName)
            fh.setFormatter(fmt)
            fh.setLevel(FileLevel)  # 日志级别

            # self.logger.addHandler(sh)
            self.logger.addHandler(fh)
        except Exception as e:
            raise e


if __name__ == '__main__':
    logger = Logger("fox",CmdLevel=logging.DEBUG, FileLevel=logging.DEBUG)
    logger.logger.debug("debug")
    logger.logger.log(logging.ERROR,'%(module)s %(info)s',{'module':'log日志','info':'error'}) #ERROR,log日志 error