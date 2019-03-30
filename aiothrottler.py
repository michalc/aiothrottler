from asyncio import (
    Future,
    get_event_loop,
)
from collections import (
    deque,
)


def Throttler(min_interval):
    loop = get_event_loop()
    queued = deque()
    last_resolved = loop.time() - min_interval
    callback = None

    def schedule_callback():
        nonlocal callback
        delay = max(0, min_interval - (loop.time() - last_resolved))
        callback = loop.call_later(delay, resolve)

    def resolve():
        nonlocal callback
        nonlocal last_resolved

        callback = None

        while queued and queued[0].cancelled():
            queued.popleft()

        if queued:
            queued.popleft().set_result(None)
            last_resolved = loop.time()

        if queued:
            schedule_callback()

    def throttler():
        future = Future()
        queued.append(future)

        if callback is None:
            schedule_callback()

        return future

    return throttler
