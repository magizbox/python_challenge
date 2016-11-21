from contextlib import contextmanager
import threading
import _thread


class TimeoutException(Exception):
    def __init__(self, msg=''):
        self.msg = msg

@contextmanager
def throw_timeout():
    raise TimeoutException("Timed out")

@contextmanager
def time_limit(seconds, msg=''):
    timer = threading.Timer(seconds, throw_timeout)
    timer.start()
    try:
        yield
    except KeyboardInterrupt:
        raise TimeoutException("Timed out for operation {}".format(msg))
    finally:
        # if the action ends in specified time, timer is canceled
        timer.cancel()
