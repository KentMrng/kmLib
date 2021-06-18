import logging
import os
import sys
import textwrap


LOGLEVEL = logging.INFO


class LogFormatter(logging.Formatter):
  
    def __init__(self, width=90, padding=10):
        super(LogFormatter, self).__init__()
        self.width = width
        self.padding = padding

    def do_wrap(self, msg, pad):
        wrapped = textwrap.wrap(msg, self.width - self.padding)
        return ['{0}{1}'.format(pad, ln) for ln in wrapped]

    def format(self, record):
        if record.levelno < 30:
            res = record.msg
        else:
            res = '\n{0} : [{1}] : {2}'.format(record.levelname, self.formatTime(record), record.pathname)
        return res


class Logger(object):

    def __init__(self, name):
        self.level = LOGLEVEL
        self.logger = logging.getLogger(name)
        if not self.logger.handlers:
            self.setHandler()

    def set_handler(self):
        self.console = logging.StreamHandler()
        self.logger.setLevel(self.level)
        self.console.setFormatter(LogFormatter())
        self.console.setLevel(logging.WARN)
        self.logger.addHandler(self.console)

    def get_logger(self):
        return self.logger

    def set_file(self, path):
        if not os.access(path, os.W_OK):
            print('ERROR: Cant write to directory {} '.format(path))
        self.log_file = path
