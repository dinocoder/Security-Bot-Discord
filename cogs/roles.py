import discord
from discord.ext import commands

class RoleModifierCog:
    
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.guild_only()
    async def joined(self, ctx, *, member: discord.Member = None):

        if not member:
            member = ctx.author
        
        await ctx.send(f'{member.display_name} joined on {member.joined_at}')
    
    @commands.command(name = 'giverole', aliases = ['addrole', 'addperms', 'giveperms', 'removerole', 'removeperms', 'takerole'])
    @commands.guild_only()
    async def changeRole(self, ctx):

        author = ctx.author
        
        if not author.guild_permissions.administrator:
            addition_commands = ('*giverole', '*addrole', '*addperms', '*giveperms')
            containment = ctx.message.content.split()[1:]
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
                roles.append(discord.utils.get(ctx.message.guild.roles, name = i))

            if len(ctx.message.mentions) > 0:
                member = ctx.message.mentions[0]
            else:
                member = discord.utils.get(ctx.message.guild.members, name = username)
                
            if ctx.message.content.startswith(addition_commands):
                for i in roles:
                    await member.add_roles(i)
            else:
                for i in roles:
                    await member.remove_roles(i)

        else:
            print("not")
            await author.send('You do not have permission to use the command `' + ctx.message.content.split()[0] + '` in ' + ctx.message.guild.name + '!')


def setup(client):
    client.add_cog(RoleModifierCog(client))
