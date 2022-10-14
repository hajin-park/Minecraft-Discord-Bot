import discord
#help
def display_help(pg):
    max_pg = 2
    embed = discord.Embed(
        title = '__Help__',
        description = '-help [#(1-2)]',
        colour = discord.Colour.blue()
    )
    embed.set_author(name = 'Page %s of %d' % (pg, max_pg))
    if pg == 1:
        embed.add_field(name='-help', value='Displays this list', inline = False)
        embed.add_field(name='-hello', value='Hello!', inline = False)
        embed.add_field(name='-roles', value='Returns givable role list', inline = False)
        embed.add_field(name='-role [role]', value='Gives you the role from the role list', inline = False)
        embed.add_field(name='-server help', value='Returns help list for server status commands', inline = False)
        return embed
    elif pg == 2:
        embed.add_field(name='-filter help', value='Returns help list for filter commands', inline = False)
        return embed

    return embed