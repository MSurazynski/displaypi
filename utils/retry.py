import time
import logging
from errors import *

logger = logging.getLogger(__name__)


def retry(operation, attempts=3, delay=1):
    """
    Attempts to perform an operation.

    Args:
        operation: function to try to perform.
        attempts: number of allowed attempts to perform operation.
        delay: delay between attempts in seconds.

    Raises:
        Any error that can be raised by operation.
    """

    last_error = None

    for attempt in range(1, attempts + 1):
        try:
            return operation()
        except (APIError, JsonError) as e:
            last_error = e
            logger.warning(
                f"Attempt {attempt} / {attempts} to run {str(operation)} failed: {e}"
            )
        if attempt < attempts:
            time.sleep(delay)

    raise last_error
