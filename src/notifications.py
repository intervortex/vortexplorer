import logging
import random

BLAME = ("Snyde", "ferday", "Tarbs")


def notify_discord(message: str) -> None:
    """Publish a message to Discord."""
    from app import REDIS
    if REDIS:
        logging.error(f"publishing to redis: {message}")
        REDIS.publish('discord', message)


def notify(message: str) -> None:
    """Notify using all available channels."""
    message = message + "\nBlame " + random.choice(BLAME)
    notify_discord(message)
    logging.error(message)
