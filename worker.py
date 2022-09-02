import os
import aioredis
import asyncio
from src.discord.discord_bot import disc_bot, intents

redis_url = os.getenv('REDISCLOUD_URL', 'redis://localhost:6379')
botty = disc_bot(intents)


async def reader(chan):
    while (await chan.wait_message()):
        msg = await chan.get(encoding="utf-8")
        await botty.print(msg)


async def listen_redis():

    await botty.wait_until_ready()

    r = await aioredis.create_redis(redis_url)
    res = await r.subscribe('discord')
    ch1 = res[0]
    tsk = asyncio.ensure_future(reader(ch1))
    await tsk

    # # gracefully closing underlying connection
    r.close()
    await r.wait_closed()


if __name__ == '__main__':
    botty.loop.create_task(listen_redis())
    botty.run_loop()
