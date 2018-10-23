# -*- coding: utf-8 -*-
import discord, sys
TOKEN = input("enter your token: ")
client = discord.Client()

channels = dict()
#Stores channels by creator name
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.author in channels:
        return
    if message.content.startswith('call'):
        call = message.content.split(' ')
    else:
        return
    if call[1] == 'die':
        for channel in iter(channels.values()):
            await client.delete_channel(channel)
        sys.exit()
    if call[1] == 'new':
        channel = await client.create_channel(message.server, "" + message.author.nick + 
                                    "\'s server", type=discord.ChannelType.voice)
        channels[message.author] = channel
        founder = discord.PermissionOverwrite()
        founder.mute_members = True
        founder.move_members = True
        
        fool = discord.PermissionOverwrite()
        fool.mute_members = False
        fool.mute_members = False
        
        for member in message.server.members:
            if member == message.author:
                await client.edit_channel_permissions(channel, member, founder)
            if member != message.author:
                await client.edit_channel_permissions(channel, member, fool)
        await client.send_message(message.channel, 'Set up a channel for ' + message.author.nick + '')
    if call[1] == 'end':
        if message.author in channels:
            await client.delete_channel(channels[message.author])
            channels.pop(message.author)
            
        await client.send_message(message.channel, 'Removed the channel for ' + message.author.nick + '')
@client.event
async def on_voice_state_update(before, after):
        if not after.voice.mute:
            for channel in iter(channels.values()):
                if after.voice.voice_channel == channel:
                    await client.server_voice_state(after, mute=True)
client.run(TOKEN)

        
