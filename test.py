import asyncio
from asyncio import (
    Event,
    ensure_future,
    get_event_loop,
)
from unittest import (
    TestCase,
)
from unittest import (
    TestCase,
)

from aiofastforward import (
    FastForward,
)
from aiothrottler import (
    Throttler,
)


def async_test(func):
    def wrapper(*args, **kwargs):
        future = func(*args, **kwargs)
        loop = get_event_loop()
        loop.run_until_complete(future)
    return wrapper


class TestThrottler(TestCase):

    @async_test
    async def test_tasks_queued_immediatly(self):
            loop = get_event_loop()

            async def func(throttle, event):
                await throttle
                event.set()

            with FastForward(loop) as forward:
                throttler = Throttler(2)

                event_a = Event()
                task_a = ensure_future(func(throttler(), event_a))

                event_b = Event()
                task_b = ensure_future(func(throttler(), event_b))

                event_c = Event()
                task_c = ensure_future(func(throttler(), event_c))

                await event_a.wait()
                await forward(1)

                self.assertFalse(event_b.is_set())
                self.assertFalse(event_c.is_set())

                await forward(1)
                await event_b.wait()
                self.assertFalse(event_c.is_set())

                await forward(1)
                self.assertFalse(event_c.is_set())

                await forward(1)
                await event_c.wait()

                task_a.cancel()
                task_b.cancel()
                task_c.cancel()

    @async_test
    async def test_tasks_queued_later(self):
            loop = get_event_loop()

            async def func(throttle, event):
                await throttle
                event.set()

            with FastForward(loop) as forward:
                throttler = Throttler(2)

                event_a = Event()
                task_a = ensure_future(func(throttler(), event_a))

                await event_a.wait()

                forward(1)

                event_b = Event()
                task_b = ensure_future(func(throttler(), event_b))

                event_c = Event()
                task_c = ensure_future(func(throttler(), event_c))

                self.assertFalse(event_b.is_set())
                self.assertFalse(event_c.is_set())

                await forward(1)
                await event_b.wait()
                self.assertFalse(event_c.is_set())

                await forward(1)
                self.assertFalse(event_c.is_set())

                await forward(1)
                await event_c.wait()

                task_a.cancel()
                task_b.cancel()
                task_c.cancel()

    @async_test
    async def test_single_task(self):
            loop = get_event_loop()

            async def func(throttler, event_a, event_b):
                await throttler()
                await asyncio.sleep(1)
                event_a.set()
                await throttler()
                event_b.set()

            with FastForward(loop) as forward:
                throttler = Throttler(2)

                event_a = Event()
                event_b = Event()
                task = ensure_future(func(throttler, event_a, event_b))

                # Yield to allow the sleep to be scheduled
                await forward(0)
                await forward(1)
                await event_a.wait()

                await forward(1)
                await event_b.wait()

                task.cancel()

    @async_test
    async def test_tasks_cancelled(self):
            loop = get_event_loop()

            async def func(throttle, event):
                await throttle
                event.set()

            with FastForward(loop) as forward:
                throttler = Throttler(1)

                event_a = Event()
                task_a = ensure_future(func(throttler(), event_a))
                task_b = ensure_future(func(throttler(), Event()))
                task_c = ensure_future(func(throttler(), Event()))
                event_d = Event()
                task_d = ensure_future(func(throttler(), event_d))

                await event_a.wait()

                task_b.cancel()
                task_c.cancel()

                await forward(1)
                await event_d.wait()

                task_a.cancel()
                task_d.cancel()
