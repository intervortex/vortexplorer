import os
import redis
import asyncio
from src.discord_bot import disc_bot

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
conn = redis.from_url(redis_url)
p = conn.pubsub()
p.subscribe('discord')

botty = disc_bot()


async def listen_redis():

    await botty.print("Starting to listen.")

    for new_message in p.listen():
        await botty.print(new_message['data'])


if __name__ == '__main__':
    asyncio.run(listen_redis())
