'''
# https://www.linux.com/blog/asynchronous-programming-python-asyncio-0

Coroutine — generator that consumes data, but doesn’t generate it. 
Python 2.5 introduced a new syntax that made it possible to send a value to a generator. 
I recommend checking David Beazley “A Curious Course on Coroutines and Concurrency” for a detailed description of coroutines.

Tasks — schedulers for coroutines. 
If you check a source code below, you’ll see that it just says event_loop to run its _step as soon as possible, 
meanwhile _step just calls next step of coroutine.

Event Loop — think of it as the central executor in asyncio.s
'''

import asyncio  
import time  
from datetime import datetime


async def custom_sleep():  
    print('SLEEP', datetime.now())
    time.sleep(1)

# the same code, but with the asynchronous sleep method:
async def custom_sleep_asyncio():  
    print('SLEEP {}\n'.format(datetime.now()))
    await asyncio.sleep(1)

async def factorial(name, number):  
    f = 1
    for i in range(2, number+1):
        print('Task {}: Compute factorial({})'.format(name, i))
        # await custom_sleep()
        await custom_sleep_asyncio()
        f *= i
    print('Task {}: factorial({}) is {}\n'.format(name, number, f))


start = time.time()  
loop = asyncio.get_event_loop()

tasks = [  
    asyncio.ensure_future(factorial("A", 7)),
    asyncio.ensure_future(factorial("B", 9)),
]
loop.run_until_complete(asyncio.wait(tasks))  
loop.close()

end = time.time()  
print("Total time: {}".format(end - start))  




# class Task(futures.Future):  
#     def __init__(self, coro, loop=None):
#         super().__init__(loop=loop)
#         # ...
#         self._loop.call_soon(self._step)

#     def _step(self):
#             # ...
#         try:
#             # ...
#             result = next(self._coro)
#         except StopIteration as exc:
#             self.set_result(exc.value)
#         except BaseException as exc:
#             self.set_exception(exc)
#             raise
#         else:
#             # ...
#             self._loop.call_soon(self._step)