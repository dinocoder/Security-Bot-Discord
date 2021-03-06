#!\zbash\bin\python3.6
import os
import discord
import asyncio
import config
from discord.ext import commands
import sys, traceback
from boto.s3.connection import S3Connection

TOKEN = os.environ.get['TOKEN']

#client = discord.Client()
client = commands.Bot(command_prefix = '*')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(game = discord.Game(name = str(len(client.users)) + ' people type *help', type=3))
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('https://discord.gg/') and message.channel != discord.utils.get(message.guild.channels, id = '468444379078459401'):
      await message.delete()
      await message.author.send("Please do not post server invite links outside of #advertise!")

    #giverole and removerole command
    if message.content.startswith('*giverole') or message.content.startswith('*removerole'):
        if message.author.guild_permissions.administrator:
            containment = message.content.split()[1:]
            username = containment[0]
            roles = []
            rolesListed = []
            processingRole = ''

            for i in containment[1:]:
                if i.endswith(','):
                    if processingRole != '':
                        rolesListed.append(processingRole[:-1])
                        processingRole = ''
                    else:
                        rolesListed.append(i.replace(',', ''))
                else:
                    processingRole += i
                    processingRole += ' '
            if processingRole != '':
                        rolesListed.append(processingRole[:-1])
                        processingRole = ''
            
            for i in rolesListed:
                roles.append(discord.utils.get(message.guild.roles, name = i))

            if len(message.mentions) > 0:
                user = message.mentions[0]
                if message.content.startswith('*giverole'):
                    for i in roles:
                        await user.add_roles(i)
                else:
                    for i in roles:
                        await user.remove_roles(i)
                return

            else:
                user = discord.utils.get(message.guild.members, name = username)

            if message.content.startswith('*giverole'):
                for i in roles:
                    await user.add_roles(i)
            else:
                for i in roles:
                    await user.remove_roles(i)

    



@client.event
async def on_member_update(before, after):

  if before.roles != after.roles:
    oldroles = before.roles
    newroles = after.roles
    
    addedroles = list(set(newroles) - set(oldroles))
    removedroles = list(set(oldroles) - set(newroles))

    channel = discord.utils.get(after.guild.channels, name = "uplodad-announcments")

    if len(addedroles) != 0:
      await channel.send(after.name + '#' + after.discriminator + ' has been given the ' + addedroles[0].name + ' role.')
    
    if len(removedroles) != 0:
      await channel.send(after.name + '#' + after.discriminator + ' has been removed of the ' + removedroles[0].name + ' role.')

client.run(TOKEN, bot = True, reconnect = True)
