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
    "Graphic design masterclass, obviously.",
    "I wish those bands put as much care into the album cover as you put in this topster.",
    "Good thing I'm a bot, otherwise that music would offend me.",
]


class disc_bot(discord.Client):

    TOKEN = None
    GUILD = None
    broadcast_chan = None
    react_litter = None
    react_yngw = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        try:
            self.TOKEN = os.environ['DISCORD_TOKEN']
        except KeyError:
            print("No token found in ENV")
            return

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        print()
        self.GUILD = discord.utils.get(
            self.guilds,
            name='Interdimensional Vortex of Conspiratorial Tastemaking'
        )
        print(f"Found Vortex {self.GUILD.name}")
        self.broadcast_chan = discord.utils.get(
            self.GUILD.text_channels, name='techxplorer'
        )
        print(f"Found broadcast channel {self.broadcast_chan.name}")
        # self.react_litter = discord.utils.get(
        #     self.GUILD.emojis, name='put_litter_in_its_place'
        # )
        self.react_yngw = discord.utils.get(self.GUILD.emojis, name='yngwie2')

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!testbot'):
            await message.reply('I am working!', mention_author=True)
            return

        if 'fuck snyde' in message.content.lower():
            await message.reply('Yeah, fuck Snyde!', mention_author=False)
            return

        if '(╯°□°）╯︵ ┻━┻' in message.content:
            await message.reply('┬─┬ ノ( ゜-゜ノ)', mention_author=False)
            return

        if 'topster' in message.content.lower():
            await message.reply(random.choice(TOPSTER), mention_author=False)
            return

        if message.content.lower().startswith('np'):
            if random.random() < 0.5:
                await message.add_reaction("🚮")
            elif self.react_yngw and random.random() < 0.3:
                await message.add_reaction(self.react_yngw)
            return

    async def print(self, text):
        if self.broadcast_chan:
            print(self.broadcast_chan)
            await self.broadcast_chan.send(text)

    def run_loop(self):
        self.run(self.TOKEN)
