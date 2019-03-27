# aiothrottler [![CircleCI](https://circleci.com/gh/michalc/aiothrottler.svg?style=svg)](https://circleci.com/gh/michalc/aiothrottler) [![Test Coverage](https://api.codeclimate.com/v1/badges/e52e294a919c8974c133/test_coverage)](https://codeclimate.com/github/michalc/aiothrottler/test_coverage)

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
