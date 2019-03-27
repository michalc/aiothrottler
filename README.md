# aiothrottler

Throttler for asyncio Python


## Installation

```base
pip install aiothrottler
```


## Example: single task throttled

```python
import asyncio
import time

from aiothrottler import Throttler

async def main():
    # Allows one resolve every 0.5 seoncds
    throttler = Throttler(0.5)
    for _ in range(10):
        await throttler()
        # Will call print 0.5 seconds after the previous call
        print(time.time())

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
```


## Example: multiple tasks throttled

```python
import asyncio
import time

from aiothrottler import Throttler

async def main():
    # Allows one resolve every 0.5 seoncds
    throttler = Throttler(0.5)
    await asyncio.gather(*[
        worker(throttler) for _ in range(10)
    ])

async def worker(throttler):
    await throttler()
    # Will call print 0.5 seconds after the previous call
    print(time.time())

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
```
