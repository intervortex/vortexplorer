import logging


def notify_discord(message: str) -> None:
    """Publish a message to Discord."""
    from app import REDIS
    if REDIS:
        REDIS.publish('discord', message)


def notify(message: str) -> None:
    """Notify using all available channels."""
    notify_discord(message)
    logging.error(message)
