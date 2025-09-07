import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

TOKEN = os.getenv("TOKEN")
PREFIX = "!"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# -------------------- Evento on_ready --------------------
@bot.event
async def on_ready():
    print(f"✅ Bot está online como {bot.user}")

# -------------------- Comando Ping --------------------
@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"🏓 Pong! Latência: {bot.latency * 1000:.2f}ms")

# -------------------- Comando Plano --------------------
@bot.command(name="plano")
async def plano(ctx):
    await ctx.send(
        "✏ **Vamos criar seu plano!**\n"
        "Digite no chat usando este formato:\n\n"
        "`!criarplano Título | Descrição | Nome1:Valor1 | Nome2:Valor2 | Rodapé | FF0000`\n\n"
        "Exemplo:\n"
        "`!criarplano Plano VIP | Acesso ilimitado | Benefício:VIP | Preço:R$50 | Obrigado por escolher! | 00FF00`"
    )

# -------------------- Comando Criar Plano --------------------
@bot.command(name="criarplano")
async def criar_plano(ctx, *, args):
    try:
        partes = [p.strip() for p in args.split("|")]

        titulo = partes[0]
        descricao = partes[1]
        campos = partes[2:-2]  # Tudo que estiver entre descrição e rodapé
        rodape = partes[-2]
        cor = int(partes[-1], 16)

        embed = discord.Embed(title=titulo, description=descricao, color=cor)

        for campo in campos:
            if ":" in campo:
                nome, valor = campo.split(":", 1)
                embed.add_field(name=nome.strip(), value=valor.strip(), inline=False)

        embed.set_footer(text=rodape)

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"❌ **Erro ao criar plano:** {e}\n"
                       "Use o formato correto: `!criarplano Título | Descrição | Nome:Valor | Rodapé | FF0000`")

# -------------------- Rodar Bot --------------------
bot.run(TOKEN)
