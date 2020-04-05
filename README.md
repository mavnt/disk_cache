# disk_cache

Disk caching decorator.

# Example
```python
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
```

```python
> python3 main.py 
2.0011584758758545
2.000434637069702
2.7179718017578125e-05
```