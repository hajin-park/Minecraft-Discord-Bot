import json
import discord
#filter
def filter_help():
    embed = discord.Embed(
        title = '__Filter Help__',
        description = 'Filter commands (Requires Admin or \"Filter\" role)',
        colour = discord.Colour.red()
    )
    embed.add_field(name = '-filter help', value = 'Returns this message\nAliases: -filter', inline = False)
    embed.add_field(name = '-filter list', value = 'Returns the list of filtered words', inline = False)
    embed.add_field(name = '-filter add [phrase]', value = 'Adds phrase to list of filtered words', inline = False)
    embed.add_field(name = '-filter remove [phrase]', value = 'Removes phrase from list of filtered words', inline = False)
    embed.add_field(name = '-filter clear', value = 'Clears list of filtered words', inline = False)
    return embed

def filter_list():
    with open('modules/filtered_words.json', 'r') as json_file:
        data = json.load(json_file)
        msg = '```\nFiltered Words - %s\n' % len(data['words'])
        for word in data['words']:
            msg = msg+word+'\n'
        msg+='```'
    return msg

def filter_word_add(word):
    with open('modules/filtered_words.json', 'r+') as json_file:
        data = json.load(json_file)

        if word in data['words']:
            return False

        data['words'].append(word)

        json_file.truncate(0)
        json_file.seek(0)
        json.dump(data, json_file, indent=4)
        
        return True

def filter_word_remove(word):
    with open('modules/filtered_words.json', 'r+') as json_file:
        data = json.load(json_file)

        if not(word in data['words']):
            return False

        data['words'].remove(word)

        json_file.truncate(0)
        json_file.seek(0)
        json.dump(data, json_file, indent=4)

        return True

def filter_clear():
    with open('modules/filtered_words.json', 'r+') as json_file:
        data = json.load(json_file)

        data['words'].clear()

        json_file.truncate(0)
        json_file.seek(0)
        json.dump(data, json_file, indent = 4)

def filter_validperms(channel, author):
    if channel.permissions_for(author).administrator:
        return True
    else:
        roles = author.roles
        for role in roles:
            if role.name.lower() == 'filter':
                return True
        return False

def filter_validphrase(msg):
    with open('modules/filtered_words.json', 'r') as json_file:
        data = json.load(json_file)
        words = data['words']
        
    for word in words:
        if word in msg.lower():
            return False
    return True