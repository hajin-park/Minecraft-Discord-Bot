import discord
import json
from datetime import datetime
from mcstatus import MinecraftServer
from mojang_api import get_uuids
#server status

ip = ''
with open('config.json') as json_file:
    data = json.load(json_file)
    ip = data['ip']
    
server = MinecraftServer.lookup('%s' % ip)

def server_status():
    server.ping()
    status = server.status()
    #now = datetime.now()
    #hour_str = now.strftime('%h')
    #time = now.strftime('%m:%s')
    #hour_mod = str(int(hour_str)%12)
    
    msg = f'```\nThe server is online. Player count: {status.players.online}```'
    #\nTime: `{}`. \n```'.format(status.players.online, '%s:%d' % (hour_mod, time))
    return msg  

def server_latency():
    latency = server.ping()
    return "The server replied in `%s ms`" % latency

def server_players():
    server.ping()
    query = server.query()
    players_online = query.players.names

    embed = discord.Embed(
        title = '__Online Players__ - %s' % len(players_online),
        colour = discord.Colour.green()
    )

    embed.set_author(name = 'Server: %s' % ip)

    if len(players_online) == 0:
        embed.add_field(name='No players online', value=':(', inline = False)
        return embed

    for player in players_online:
        p = get_uuids(username=player)
        embed.add_field(name=player, value='UUID: %s' % p.uuid, inline = False)

    return embed