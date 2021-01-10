import os
import discord


class disc_bot(discord.Client):

    TOKEN = None
    GUILD = ""

    def __init__(self) -> None:
        super().__init__()

        try:
            os.environ['DISCORD_TOKEN']
        except KeyError:
            print("no can do")
            pass

        self.run(self.TOKEN)
        print("Discord is fine")

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
