import discord
import asyncio
import time
import re
import config

Client = discord.Client()
client = commands.Bot(command_prefix = '')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(status=discord.Status.idle, activity=discord.Watching('people type *help'))

@client.event
async def on_message(message):

    if message.author == client.user:
        return
    
    if message.content.startswith('https://discord.gg/') and message.channel != discord.utils.get(message.guild.channels, id = '468444379078459401'):
      await message.delete()
      await client.send_message(message.author, "Please do not post server invite links outside of #advertise!")

    if message.content.startswith('*giverole'):
      args = message.content.split()[:1]
      user = args[0]
      roles = args[:1]

      if len(message.mentions) > 0:
        message.mentions[0].add_roles(roles)
      #else
        




@client.event
async def on_member_update(before, after):

  if before.roles != after.roles:
    oldroles = before.roles
    newroles = after.roles
    
    addedroles = set(newroles) - set(oldroles)
    removedroles = set(oldroles) - set(newroles)

    channel = discord.utils.get(after.guild.channels, id = '468443757319028737')

    if addedroles.length != 0:
      await channel.send(after.name + '#' + after.discriminator + ' has been given the ' + addedroles[0] + ' role.')
    
    if removedroles.length != 0:
      await channel.send(after.name + '#' + after.discriminator + ' has been removed of the ' + removedroles[0] + ' role.')

client.run(config.token)
