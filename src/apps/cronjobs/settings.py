import logging

schedule_logger = logging.getLogger('schedule')
schedule_logger.setLevel(level=logging.ERROR)

logging.getLogger('emcache').setLevel(level=logging.ERROR)