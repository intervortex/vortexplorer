import os
import discord


class disc_bot(discord.Client):

    TOKEN = os.environ['DISCORD_TOKEN']
    GUILD = ""

    def __init__(self) -> None:
        super().__init__()
        self.run(self.TOKEN)

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        for chan in self.get_all_channels():
            print(chan.name)
            if chan.name == 'general':
                self.broadcast_chan = chan
                print(f"found channel {chan}")

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!testbot'):
            await message.reply('Hello!', mention_author=True)
            await self.print("I am working")

    async def print(self, text):
        await self.broadcast_chan.send(text)
