import os
import pickle
import time
from functools import wraps
from threading import Thread, Lock
from typing import Dict, List

from .logging_utils import logger

decorator_with_args = lambda d: lambda *args, **kwargs: lambda func: wraps(func)(
    d(func, *args, **kwargs)
)


def write_to_file(cache, f_name, lock, index, it_is_too_late, sleep_time):
    log_prefix = f"t{index} for {f_name}:"
    logger.debug(f"{log_prefix} sleeping for {sleep_time}")
    time.sleep(sleep_time)
    if not it_is_too_late[index] and not lock.locked():
        with lock:
            with open(f_name, "wb") as f:
                pickle.dump(cache, f)
                logger.debug(f"{log_prefix} written to file")
    else:
        logger.debug(f"{log_prefix} too late or lock taken")


@decorator_with_args
def disk_cache(function, directory=".", sleep_time=2.5):
    lock: Dict[str, Lock] = {}
    cache: Dict[str, dict] = {}
    cache_miss: Dict[str, bool] = {}
    it_is_too_late: Dict[str, List[bool]] = {}
    i: Dict[str, int] = {}

    @wraps(function)
    def wrapper(*args, **kwargs):
        fu_name = function.__name__
        fi_name = os.path.join(directory, f"{fu_name}.cache")
        lock[fu_name] = lock.get(fu_name, Lock())
        cache[fu_name] = cache.get(fu_name, {})
        cache_miss[fu_name] = cache_miss.get(fu_name, {})
        it_is_too_late[fu_name] = it_is_too_late.get(fu_name, [])
        i[fu_name] = i.get(fu_name, 0)

        if len(cache[fu_name]) == 0 and os.path.isfile(fi_name):
            with open(fi_name, "rb") as f:
                cache[fu_name] = pickle.load(f)
        key = (
            args,
            tuple(sorted(kwargs.items(), key=lambda x: hash(x))),
        )
        if key not in cache[fu_name]:
            logger.debug(f"cache miss for {fu_name}")
            cache[fu_name][key] = function(*args, **kwargs)
            cache_miss[fu_name] = True
        if cache_miss[fu_name]:
            if i[fu_name] > 0:
                it_is_too_late[fu_name][-1] = True
            it_is_too_late[fu_name].append(False)
            Thread(
                target=write_to_file,
                args=(
                    cache[fu_name],
                    fi_name,
                    lock[fu_name],
                    i[fu_name],
                    it_is_too_late[fu_name],
                    sleep_time,
                ),
            ).start()
            cache_miss[fu_name] = False
            i[fu_name] += 1
        return cache[fu_name][key]

    return wrapper


if __name__ == "__main__":
    pass
