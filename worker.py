import os
import redis
import aioredis
import asyncio
from src.discord_bot import disc_bot

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
botty = disc_bot()


# async def reader(ch):
#     while (await ch.wait_message()):
#         msg = await ch.get()
#         await botty.print(msg['data'])
async def main():

    print("going for the listen thing")
    await botty.print("Starting to listen.")
    print("back from the listen thing")

    # conn = await aioredis.create_connection(redis_url)
    # res = await conn.subscribe('discord')
    # ch1 = res[0]
    # tsk = asyncio.ensure_future(reader(ch1))
    # await tsk

    # # gracefully closing underlying connection
    # conn.close()
    # await conn.wait_closed()


if __name__ == '__main__':
    asyncio.run(main())
