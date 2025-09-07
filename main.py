import discord
import os
from dotenv import load_dotenv

load_dotenv()

GUILD_ID = 895003881820524604
bot = discord.Bot(intents=discord.Intents.all())

# -------------------- Modal --------------------
class PlanoModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Criar Embed do Plano")

        self.add_item(discord.ui.TextInput(label="Título", placeholder="Digite o título do embed"))
        self.add_item(discord.ui.TextInput(label="Descrição", placeholder="Digite a descrição", style=discord.TextStyle.paragraph))
        self.add_item(discord.ui.TextInput(label="Campos (use | para separar)", placeholder="Ex: Nome:Valor | Nome:Valor"))
        self.add_item(discord.ui.TextInput(label="Rodapé", placeholder="Digite o rodapé"))
        self.add_item(discord.ui.TextInput(label="Cor (hex sem #)", placeholder="Ex: FF0000 para vermelho"))

    async def on_submit(self, interaction: discord.Interaction):
        try:
            titulo = self.children[0].value
            descricao = self.children[1].value
            campos = self.children[2].value
            rodape = self.children[3].value
            cor = int(self.children[4].value, 16) if self.children[4].value else 0x3498db

            embed = discord.Embed(title=titulo, description=descricao, color=cor)

            if campos:
                for campo in campos.split("|"):
                    if ":" in campo:
                        nome, valor = campo.split(":", 1)
                        embed.add_field(name=nome.strip(), value=valor.strip(), inline=False)

            embed.set_footer(text=rodape)

            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao criar embed: {e}", ephemeral=True)

# -------------------- Evento --------------------
@bot.event
async def on_ready():
    print(f"✅ Bot online como {bot.user}!")

# -------------------- Comando /ping --------------------
@bot.slash_command(name="ping", description="Responde com Pong!")
async def ping(ctx):
    await ctx.respond(f"Pong! {bot.latency * 1000:.2f}ms")

# -------------------- Comando /plano --------------------
@bot.slash_command(name="plano", description="Crie um embed personalizado para planos")
async def plano(ctx):
    try:
        await ctx.send_modal(PlanoModal())
    except Exception as e:
        await ctx.respond(f"❌ Erro ao abrir modal: {e}", ephemeral=True)

# -------------------- Rodar Bot --------------------
bot.run(os.getenv("TOKEN"))
