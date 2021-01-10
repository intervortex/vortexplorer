import os
import redis
from src.discord_bot import disc_bot

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
conn = redis.from_url(redis_url)
botty = disc_bot()

if __name__ == '__main__':

    p = conn.pubsub()
    p.subscribe('discord')

    for new_message in p.listen():
        botty.print(new_message['data'])
