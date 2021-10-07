import logging


def configure_http_request_logging(log_level=logging.INFO):
    logger = logging.getLogger('urllib3')
    logger.setLevel(log_level)
    logger.propagate = True
