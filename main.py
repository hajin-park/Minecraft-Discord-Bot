'''
Discord bot
'''
import discord
from discord.ext import commands
import logging
import json

import modules.server as module_server
import modules.roles as module_roles
import modules.filter as module_filter
import modules.help as module_help


class DiscordBot(discord.Client):

    #Initialize bot instance
    def __init__(self) -> None:
        super().__init__()
        logging.basicConfig(level=logging.INFO)
        self.client = commands.Bot(command_prefix = '!')
        self.client.remove_command('help')

        with open('config.json') as json_file:
            data = json.load(json_file)
            self.client.run(data['token'])

        @self.client.event
        async def on_ready():
            print('We have logged in as {0.user}'.format(self.client))
            await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!help"))

    #User commands
    def user_commands(self):
        pass

    #Admin commands
    def admin_commands(self):
        pass

    #Respond to errors
    def error(self):
        @client.event
        async def on_message(message):
            if message.author == client.user:
                await client.process_commands(message)
                return
            if message.content.strip().startswith('-'):
                await client.process_commands(message)
                return
            elif not module_filter.filter_validphrase(message.content):
                await message.channel.send('<@%s>, bruh don\'t say that' % message.author.id)
                await message.delete()
            await client.process_commands(message)

        @client.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.CommandNotFound):
                await ctx.send('Command not found. See -help.')
                return
            if isinstance(error, commands.MissingRequiredArgument):
                await ctx.send('Missing argument. See -help.')
                return


if __name__ == "__main__":
    bot = DiscordBot()

#---------------------------#
    
'''@client.command()
async def roles(ctx):
    embed = module_roles.roles_list(ctx.guild.roles)
    await ctx.send(embed)

@client.command()
async def role(ctx, *, role):
    role_to_assign = module_roles.roles_find(ctx.author.guild.roles, role)
    if role_to_assign == None:
        await ctx.send('Role not eligible')
        return
    if role_to_assign in ctx.author.roles:
        await ctx.send('You already have that role')
        return
    await ctx.send('Gave you `%s`' % role_to_assign.name)  
    await discord.Member.add_roles(ctx.author, role_to_assign)

#---------------------------#

@client.command()
async def server(ctx, *args):
    if len(args) == 0:
        msg = '```\n-server status : Returns server status (i.e. online/offline)\n-server latency : Returns server latency\n-server players : Returns players online```'
        await ctx.send(msg)
        return
    elif len(args) == 1:
        arg = args[0]
        if arg == 'help':
            msg = '```\n-server status : Returns server status (i.e. online/offline)\n-server latency : Returns server latency\n-server players : Returns players online```'
            await ctx.send(msg)
            return
        elif arg == 'status':
            embed = module_server.server_status()
            await ctx.send(embed)
            return
        elif arg == 'latency':
            embed = module_server.server_latency()
            await ctx.send(embed)
            return
        elif arg == 'players':
            await ctx.send(embed = module_server.server_players())
            return
        else:
            await ctx.send('Invalid Argument, see -server help')
            return
    elif len(args) > 1:
        raise commands.MissingRequiredArgument()
        return

@server.error
async def server_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Missing Argument, see -server help')
        return
    err_name = error.original.__class__.__name__
    if err_name == 'ConnectionRefusedError' or err_name == 'timeout' or err_name == 'gaierror':
        await ctx.send('Server Is Offline')
        return

#---------------------------#

@client.command()
async def filter(ctx, *args):
    if len(args) == 0:
        await ctx.send(embed = module_filter.filter_help())
        return
    elif len(args) == 1:
        if args[0] == 'help':
            await ctx.send(embed = module_filter.filter_help())
            return
        elif args[0] == 'list':
            await ctx.send(module_filter.filter_list())
            return
    if module_filter.filter_validperms(ctx.message.channel, ctx.author):
        if len(args) == 1:
            if args[0] == 'clear':
                module_filter.filter_clear()
                await ctx.send('List cleared!')
                return
            elif args[0] == 'add':
                raise Exception()
                return
        elif len(args) > 1:
            if args[0] == 'add':
                word = ' '.join(args[1:])
                added = module_filter.filter_word_add(word.lower())
                if added:
                    await ctx.send('Phrase added!')
                    return
                else:
                    await ctx.send('Phrase already added.')
                    return
            elif args[0] == 'remove':
                word = ' '.join(args[1:])
                removed = module_filter.filter_word_remove(word.lower())
                if removed:
                    await ctx.send('Phrase removed!')
                    return
                else:
                    await ctx.send('Phrase not in list.')
                    return
    else:
        await ctx.send('You don\'t have permission! Only admins or `Filter` role can access this command.')

@filter.error
async def filter_error(ctx, error):
    await ctx.send('Something went wrong :/ see -filter help.')

#---------------------------#

@client.command()
async def help(ctx, *args):
    max_pg = 2
    if len(args) == 0:
        embed = module_help.display_help(1)
        await ctx.send(embed = embed)
        return

    elif len(args) == 1:
        if args[0].isalpha():
            await ctx.send('Please enter a valid number in the range 1 to %s.' % 2)
            raise ValueError()

        pg = int(args[0])
        if pg < 1 or pg > max_pg:
            await ctx.send('Please enter a valid number in the range 1 to %s.' % 2)
            return

        embed = module_help.display_help(pg)
        await ctx.send(embed = embed)
        return

    else:
        await ctx.send('Please enter a valid number in the range 1 to %s.' % 2)
        raise ValueError()
    

@help.error
async def help_error(ctx, error):
    if isinstance(error, ValueError):
        await ctx.send('Please enter a valid number in the range 1 to %s.' % 2)
        return

#---------------------------#
'''
