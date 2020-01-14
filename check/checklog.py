# encoding:utf-8
from django.conf import settings
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'db_monitor.settings')

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logfile = settings.CHECK_LOG_DIR + '/check.log'

fh = logging.FileHandler(logfile,mode='a')
fh.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)
