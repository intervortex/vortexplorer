import os
import discord
import random

TOPSTER = [
    "That's just like, your opinion, man...",
    "Might as well add Cardi B to that list.",
    "Good stuff, shame the design sucks balls.",
    "Don't 👏 talk 👏 about 👏 your 👏 topster 👏 unless 👏 Emily Montes is #1 👏",
    "You should probably reconsider your music taste.",
    "I'd rather hang myself than hang that on my wall.",
    "🙄🙄🙄🙄",
    "🙄🙄🙄🙄",
    "Topstop already",
    "More like STOPster.",
    "no u",
    "no u",
]


class disc_bot(discord.Client):

    TOKEN = None
    GUILD = None
    broadcast_chan = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        try:
            self.TOKEN = os.environ['DISCORD_TOKEN']
        except KeyError:
            print("No token found in ENV")
            return

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        for chan in self.get_all_channels():
            print(chan.name)
            if chan.name == 'techxplorer':
                self.broadcast_chan = chan
                print(f"found channel {chan}")

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!testbot'):
            await message.reply('I am working!', mention_author=True)
            return

        if message.content.startswith('!fucksnyde'):
            await message.reply('Yeah, fuck Snyde!', mention_author=False)
            return

        if '(╯°□°）╯︵ ┻━┻' in message.content:
            await message.reply('┬─┬ ノ( ゜-゜ノ)', mention_author=False)
            return

        if 'topster' in message.content.lower():
            await message.reply(random.choice(TOPSTER), mention_author=False)
            return

    async def print(self, text):
        if self.broadcast_chan:
            print(self.broadcast_chan)
            await self.broadcast_chan.send(text)

    def run_loop(self):
        self.run(self.TOKEN)
