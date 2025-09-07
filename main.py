import discord
import os
from dotenv import load_dotenv

load_dotenv()

GUILD_ID = 895003881820524604  # ID do seu servidor
bot = discord.Bot(intents=discord.Intents.all())

# -------------------- Modal para /plano --------------------
class PlanoModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Criar Embed do Plano")

        self.add_item(discord.ui.TextInput(label="Título", placeholder="Digite o título do embed"))
        self.add_item(discord.ui.TextInput(label="Descrição", placeholder="Digite a descrição", style=discord.TextStyle.paragraph))
        self.add_item(discord.ui.TextInput(label="Campos (use | para separar)", placeholder="Ex: Nome:Valor | Nome:Valor"))
        self.add_item(discord.ui.TextInput(label="Rodapé", placeholder="Digite o rodapé"))
        self.add_item(discord.ui.TextInput(label="Cor (hex sem #)", placeholder="Ex: FF0000 para vermelho"))

    async def on_submit(self, interaction: discord.Interaction):
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

# -------------------- Evento on_ready --------------------
@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    await bot.tree.sync(guild=guild)  # sincroniza os comandos apenas nesse servidor
    print(f"Bot online! {bot.user}")

# -------------------- Comando /ping --------------------
@bot.tree.command(name="ping", description="Pong!")
@discord.app_commands.guilds(discord.Object(id=GUILD_ID))
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {bot.latency*1000:.2f}ms")

# -------------------- Comando /plano --------------------
@bot.tree.command(name="plano", description="Crie um embed personalizado para planos")
@discord.app_commands.guilds(discord.Object(id=GUILD_ID))
async def plano(interaction: discord.Interaction):
    await interaction.response.send_modal(PlanoModal())

# -------------------- Rodar Bot --------------------
bot.run(os.getenv("TOKEN"))
