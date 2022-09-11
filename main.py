import discord
from discord.ext import commands
import os
import datetime
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="$")
ID_TOKEN = os.getenv('DISCORD_TOKEN')

#  Bot start 
@client.event
async def on_ready():
    print('We have logged in as {0.user} has connected to Discord!'.format(client))
    print('-----------------------------------------------------------')


#  New Member Join Notification
@client.event
async def on_member_join(member):
    mention = member.mention
    guild = member.guild
    await member.create_dm()
    await member.dm_channel.send(str(f'{mention}, Welcome on the new server {guild}').format(mention=mention, guild=guild))

    embed = discord.Embed(title=str("***New Member Joined***"), colour=0x33c946, description=str(f'{mention} joined to the {guild}').format(mention=mention, guild=guild))
    embed.set_thumbnail(url=f'{member.avatar_url}')
    embed.set_author(name=f'{member.name}', icon_url=f'{member.avatar_url}')
    embed.set_footer(text=f'{member.guild}', icon_url=f'{member.guild.icon_url}')
    embed.timestamp=datetime.datetime.utcnow()
    embed.add_field(name='User ID :', value=member.id, inline=False)
    embed.add_field(name='User Name :', value=member.display_name, inline=True)
    embed.add_field(name='Server Name :', value=guild, inline=True)
    embed.add_field(name='User Serial :', value=len(list(guild.members)), inline=True)
    embed.add_field(name='Created_at :', value=member.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'), inline=True)
    embed.add_field(name='Joined_at :', value=member.joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'), inline=True)
    
    channel = discord.utils.get(member.guild.channels, name='join-member')
    await channel.send(embed=embed)


#  Member Leave Notification
@client.event
async def on_member_remove(member):
    mention = member.mention
    guild = member.guild

    embed = discord.Embed(title=str("***New Member Leaved***"), colour=0x33c946, description=str(f'{mention} leave from {guild}').format(mention=mention, guild=guild))
    embed.set_thumbnail(url=f'{member.avatar_url}')
    embed.set_author(name=f'{member.name}', icon_url=f'{member.avatar_url}')
    embed.set_footer(text=f'{member.guild}', icon_url=f'{member.guild.icon_url}')
    embed.timestamp=datetime.datetime.utcnow()
    embed.add_field(name='User ID :', value=member.id, inline=False)
    embed.add_field(name='User Name :', value=member.display_name, inline=True)
    embed.add_field(name='Server Name :', value=guild, inline=True)
    embed.add_field(name='User Serial :', value=len(list(guild.members)), inline=True)
    embed.add_field(name='Created_at :', value=member.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'), inline=True)
    embed.add_field(name='leaved_at :', value=member.joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'), inline=True)
    
    channel = discord.utils.get(member.guild.channels, name='leave-member')
    await channel.send(embed=embed)

@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel_message = str(message.channel)
    list_in = ['hi','hello','slt','salut','bonjour','hola']
    list_out = ['bye','goodby','ciao','au revoir']
    money_user = []
    money_bot = []

    #print(f'{username}: {user_message} ({channel_message})')

    if message.author == client.user:
        return
    
    if message.content in list_in:
        await message.channel.send(f'Hello {username}!')
        return
    elif message.content in list_out:
        await message.channel.send(f'Goodbye {username}!')
        return

client.run(ID_TOKEN) 
