# aiothrottler [![CircleCI](https://circleci.com/gh/michalc/aiothrottler.svg?style=svg)](https://circleci.com/gh/michalc/aiothrottler) [![Test Coverage](https://api.codeclimate.com/v1/badges/e52e294a919c8974c133/test_coverage)](https://codeclimate.com/github/michalc/aiothrottler/test_coverage)

Throttler for asyncio Python


## Installation

```bash
pip install aiothrottler
```


## Usage

Create a shared `Throttler`, passing a minimum interval, e.g. `0.5` seconds

```python
throttler = Throttler(0.5)
```

and then just before the piece(s) of code to be throttled, _call_ this and `await` its result.

```python
await throttler()
# Execution will reach here every 0.5 seconds
```


## Example: multiple tasks throttled

```python
import asyncio
import time

from aiothrottler import Throttler

async def main():
    throttler = Throttler(0.5)
    await asyncio.gather(*[
        worker(throttler) for _ in range(10)
    ])

async def worker(throttler):
    await throttler()
    # Interval of at least 0.5 seconds between prints
    # even though all workers started together
    print(time.time())

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
```


## Example: single task throttled/smoothed

```python
import asyncio
import random
import time

from aiothrottler import Throttler

async def main():
    throttler = Throttler(0.5)
    for _ in range(10):
        await throttler()
        # Interval of at least 0.5 seconds between prints
        # even though each sleep is random
        print(time.time())
        await asyncio.sleep(random.random())

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
```


## Differences to alternatives

- The API features a function to call to `await` its result [some use a context manager]

- The API is imperative [some use a functional approach/higher-order function]

- No polling is used [some use polling internally]

- A _minimum interval between resolutions_ is used to throttle [rather that a _max resolutions per time interval_, which can cause an irregular pattern of resolutions]
