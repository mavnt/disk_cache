import time

from disk_cache import disk_cache


# @disk_cache("/dev/shm")
@disk_cache()
def slow_func(n):
    import time

    time.sleep(2)
    return 0


def main():
    # this takes ~2s for n=0
    start = time.time()
    result = slow_func(0)
    print(time.time() - start)

    
    # this takes ~2s for n=1
    start = time.time()
    result = slow_func(1)
    print(time.time() - start)

    # this is fast since slow_func(n=0) was already computed
    start = time.time()
    result = slow_func(0)
    print(time.time() - start)


if __name__ == "__main__":
    main()
