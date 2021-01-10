import os
import redis
import aioredis
import asyncio
from src.discord_bot import disc_bot

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
botty = disc_bot()


async def reader(chan):
    while (await chan.wait_message()):
        msg = await chan.get()
        print(msg)
        await botty.print(msg)


async def listen_redis():
    await botty.wait_until_ready()

    print("going for the listen thing")
    await botty.print("Starting to listen.")
    print("back from the listen thing")

    r = await aioredis.create_redis(redis_url)
    res = await r.subscribe('discord')
    ch1 = res[0]
    tsk = asyncio.ensure_future(reader(ch1))
    await tsk

    # # gracefully closing underlying connection
    r.close()
    await r.wait_closed()
    print("all finished")


if __name__ == '__main__':
    botty.loop.create_task(listen_redis())
    botty.run_loop()
