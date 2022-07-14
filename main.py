# https://github.com/juliankoh/ribbon-discord-bot
# https://github.com/melenxyz/abracadabra-tvl-bot

import discord
from discord.ext import tasks
import os
from dotenv import load_dotenv
import requests
import json
import aiohttp

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
REFRESH_TIMER = os.getenv('REFRESH_TIMER')
CONTRACT = os.getenv('CONTRACT')
NAME = os.getenv('NAME')
CHAIN = os.getenv('CHAIN')
CURRENCY = os.getenv('CURRENCY')

client = discord.Client()

async def get_price():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.coingecko.com/api/v3/simple/token_price/{CHAIN}?contract_addresses={CONTRACT}&vs_currencies={CURRENCY}") as r:
            if r.status == 200:
                js = await r.json()
                price = js[CONTRACT][CURRENCY]
                pricestring = (f"{NAME}: ${price}")
                return pricestring

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord! ')
    for guild in client.guilds:
        print("connected to ", guild.name)
    refresh_price.start()

@tasks.loop(seconds=float(REFRESH_TIMER))
async def refresh_price():
    for guild in client.guilds:
        await guild.me.edit(nick=await get_price())

def get_price_change():
    response = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=creo-engine")
    json_data = json.loads(response.text)
    pricechange = json_data['price_change_percentage_24h']
    return (pricechange)
status = get_price_change()    

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord! ')
    for guild in client.guilds:
        print("connected to ", guild.name)
    refresh_pricechange.start()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"${status}%|CREO"))

@client.event
async def on_message(message):
    if msg.startswith("!refresh"):
        refresh = get_price_change()
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"${refresh}"))
client.run(TOKEN)
