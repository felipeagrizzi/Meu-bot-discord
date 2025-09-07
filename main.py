import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

bot = discord.Bot(intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot está online!")

@bot.slash_command(name="ping", description="Pong!")
async def ping(ctx):
    await ctx.respond(f"Pong! {bot.latency * 1000:.2f}ms")

bot.run(os.getenv("TOKEN"))