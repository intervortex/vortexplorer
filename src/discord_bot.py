import os
import discord


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

    async def print(self, text):
        if self.broadcast_chan:
            print(self.broadcast_chan)
            await self.broadcast_chan.send(text)

    def run_loop(self):
        self.run(self.TOKEN)
