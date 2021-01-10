import os
import redis
import aioredis
import asyncio
from src.discord_bot import disc_bot

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
botty = disc_bot()


# conn = redis.from_url(redis_url)
# p = conn.pubsub()
# p.subscribe('discord')
async def reader(ch):
    while (await ch.wait_message()):
        msg = await ch.get()
        await botty.print(msg['data'])


async def main():

    await botty.print("Starting to listen.")

    conn = await aioredis.create_connection(redis_url)
    res = await conn.subscribe('discord')
    ch1 = res[0]
    tsk = asyncio.ensure_future(reader(ch1))
    await tsk

    # gracefully closing underlying connection
    conn.close()
    await conn.wait_closed()


if __name__ == '__main__':
    asyncio.run(main())
