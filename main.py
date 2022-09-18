import discord
import os
import datetime
import sys
import requests
import json
from discord.ext import commands
from dotenv import load_dotenv
from bs4 import BeautifulSoup
load_dotenv()

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="$")
ID_TOKEN = os.getenv('DISCORD_TOKEN')

#### URL ####
url_anssi_alert = "https://www.cert.ssi.gouv.fr/alerte/"


#### Bot start #### 
@client.event
async def on_ready():
    print('We have logged in as {0.user} has connected to Discord!'.format(client))
    print('-----------------------------------------------------------')

#### Anssi alerts ####
    await client.wait_until_ready()
    channel = client.get_channel(id_channel)
    anssi = await anssi_alerts()
    if anssi:
        for key, value in anssi.items():
            link = url_anssi_alert + key
            await channel.send(key + ": " + value[0] + " - " + value[1] + " - " + value[2] + "\n" + link + "\n" + value[3])

async def anssi_alerts():
	toReturn = {}
	infos_liste = {}
	line_in_file = []
	item_to_del = []
	###cle -> item-ref, value -> date, title, status, pdf
	url = "https://www.cert.ssi.gouv.fr"
	page = requests.get(url)
	soup = BeautifulSoup(page.content, "html.parser")
	cert_alert = soup.find_all("div", class_="cert-alert")
	###cert_alert[0] est le titre de la section
	for i in range(1,len(cert_alert)):
		date = cert_alert[i].find("span", class_="item-date")
		link = cert_alert[i].find("span", class_="item-ref")
		title = cert_alert[i].find("span", class_="item-title")
		status = cert_alert[i].find("span", class_="item-status")
		pdf = cert_alert[i].find("a", class_="item-link")
		
		infos_liste[link.text] = []
		infos_liste[link.text].append(date.text)
		infos_liste[link.text].append(title.text)
		infos_liste[link.text].append(status.text)
		if pdf is not None:
			infos_liste[link.text].append(url+pdf['href'])
		else:
			infos_liste[link.text].append("")

	if not os.path.isfile("path_file_txt"):
		f = open("path_file_txt", "w")
		for key, value in infos_liste.items():
			f.write(key+"\n")
		f.close()
		toReturn = infos_liste
	else:
		with open("path_file_txt") as f:
			for line in f:
				line_in_file.append(line.rstrip("\n"))
		for key, value in infos_liste.items():
			if key not in line_in_file:
				line_in_file.append(key)
				toReturn[key] = infos_liste[key]
		for line in line_in_file:
			if line not in infos_liste.keys():
				item_to_del.append(line)
		for item in item_to_del:
			line_in_file.remove(item)
		f = open("path_file_txt", "w")
		for line in line_in_file:
			f.write(line+"\n")
		f.close()

	return toReturn

#### New Member Join Notification ####
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


#### Member Leave Notification ####
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
