import time
from .log import getLogger
logger = getLogger(__name__)


def with_retry(retry, wait, func, *args):
    for i in range(retry):
        try:
            return func(*args)
        except Exception as exc:
            logger.info(exc)
        finally:
            time.sleep(wait)
