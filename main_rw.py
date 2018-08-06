import discord
import asyncio
import config
from discord.ext import commands
import sys, traceback

#client = commands.Bot(command_prefix = '')


def getCmdPrefix(client, message):
    
    prefixes = ['*']

    return commands.when_mentioned_or(*prefixes)(client, message)

initial_extensions = ['cogs.roles']

client = commands.Bot(command_prefix=getCmdPrefix, description='A Rewrite Cog Example')

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(game = discord.Game(name = str(len(client.users)) + ' people stype *help', type=3))

client.run(config.token, bot=True, reconnect=True)
