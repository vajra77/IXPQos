from .config import APP_CONFIG
from datetime import datetime


class Logger:

    def __init__(self):
        pass

    @classmethod
    def info(cls, msg):
        logstr = "[INFO]: {}".format( msg)
        cls._log(logstr)

    @classmethod
    def warn(cls, msg):
        logstr = "[WARN]: {}".format(msg)
        cls._log(logstr)

    @classmethod
    def crit(cls, msg):
        logstr = "[CRIT]: {}".format(msg)
        cls._log(logstr)

    @staticmethod
    def _log(msg: str):
        timestamp = datetime.today()
        logstr = "{} {}\n".format(timestamp, msg)
        f = open(APP_CONFIG['logfile'],'a')
        f.write(logstr)
        f.close()