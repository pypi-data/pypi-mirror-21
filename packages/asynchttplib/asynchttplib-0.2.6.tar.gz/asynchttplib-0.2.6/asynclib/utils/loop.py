import uvloop
import asyncio


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

get_event_loop = asyncio.get_event_loop