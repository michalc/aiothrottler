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
    resolve_callback = None

    def schedule_resolve():
        nonlocal resolve_callback
        delay = max(0, min_interval - (loop.time() - last_resolved))
        resolve_callback = loop.call_later(delay, resolve)

    def resolve():
        nonlocal resolve_callback
        nonlocal last_resolved

        resolve_callback = None

        while queued and queued[0].cancelled():
            queued.popleft()

        if queued:
            queued.popleft().set_result(None)
            last_resolved = loop.time()

        if queued:
            schedule_resolve()

    def throttler():
        future = Future()
        queued.append(future)

        if resolve_callback is None:
            schedule_resolve()

        return future

    return throttler
