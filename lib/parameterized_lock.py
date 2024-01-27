import threading
from contextlib import contextmanager

namespace_lock = threading.Lock()
namespace = {}
counters = {}


@contextmanager
def parameterized_lock(value, blocking=True, timeout=-1.0):
    try:
        with namespace_lock:
            if value in namespace:
                counters[value] += 1
            else:
                namespace[value] = threading.Lock()
                counters[value] = 1

        yield namespace[value].acquire(blocking=blocking, timeout=timeout)
    finally:
        with namespace_lock:
            if counters[value] == 1:
                del counters[value]
                lock = namespace.pop(value)
            else:
                counters[value] -= 1
                lock = namespace[value]
        lock.release()
