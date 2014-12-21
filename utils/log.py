import logging
from ju_setting import LOG_PATH

def get_file_logger(name, format='%(asctime)s %(levelname)s\n%(message)s\n', level=logging.DEBUG):
    log = logging.getLogger(name)
    if not log.handlers:
        handler = logging.FileHandler('%s/%s.log' % (LOG_PATH, name))
        formatter = logging.Formatter(format)
        handler.setFormatter(formatter)
        log.addHandler(handler)
        log.setLevel(level)
    return log