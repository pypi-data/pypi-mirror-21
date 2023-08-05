import time

from falsy.netboy.request import request
import asyncio as aio


async def boy(urls):
    targets = []
    for payload in urls:
        targets.append(request(payload))
    begin = time.time()
    res = await aio.gather(
        *targets, return_exceptions=True
    )
    end = time.time()
    print('time:', end - begin)
    # return [t.result() for t in targets]
    return res
