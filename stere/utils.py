import time
from functools import reduce
from typing import Callable, Optional

from stere import Stere


def rgetattr(obj, attr, *args):
    """A nested getattr"""
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return reduce(_getattr, [obj] + attr.split('.'))


def _retry(
    fn: Callable[[], bool], retry_time: Optional[int] = None,
) -> bool:
    """Retry a function for a specific amount of time.

    Returns:
        True if the function returns a truthy value, else False

    Arguments:
        fn (function): Function to retry
        retry_time: Number of seconds to retry. If not specified,
            Stere.retry_time will be used.

    """
    retry_time = retry_time or Stere.retry_time
    end_time = time.time() + retry_time

    # Do..while if retry_time = 0 the loop runs once
    while True:
        if fn():
            return True
        if time.time() < end_time:
            break
    return False
