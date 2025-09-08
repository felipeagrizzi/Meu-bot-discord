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

        self.add_item(discord.ui.TextInput(label="Título", placeholder="Digite o título do embed", required=False))
        self.add_item(discord.ui.TextInput(label="Descrição", placeholder="Digite a descrição", style=discord.TextStyle.paragraph, required=False))
        self.add_item(discord.ui.TextInput(label="Campos (use | para separar, ex: Nome:Valor | Nome:Valor)", style=discord.TextStyle.paragraph, required=False))
        self.add_item(discord.ui.TextInput(label="Rodapé", placeholder="Digite o rodapé", required=False))
        self.add_item(discord.ui.TextInput(label="Cor (hex sem #)", placeholder="Ex: FF0000 para vermelho", required=False))
        self.add_item(discord.ui.TextInput(label="Link da imagem (opcional)", placeholder="Cole o link da imagem", required=False))

    async def on_submit(self, interaction: discord.Interaction):
        titulo = self.children[0].value or "Título Padrão"
        descricao = self.children[1].value or "Descrição padrão"
        campos = self.children[2].value
        rodape = self.children[3].value or ""
        cor = int(self.children[4].value, 16) if self.children[4].value else 0x000000
        imagem = self.children[5].value

        embed = discord.Embed(
            title=f"**{titulo}**", 
            description=f"**{descricao}**", 
            color=cor
        )

        if campos:
            for campo in campos.split("|"):
                if ":" in campo:
                    nome, valor = campo.split(":", 1)
                    embed.add_field(name=f"**{nome.strip()}**", value=valor.strip(), inline=False)

        embed.set_footer(text=rodape)

        if imagem:
            embed.set_image(url=imagem)

        await interaction.response.send_message(embed=embed, ephemeral=True)  # Só o usuário vê

# -------------------- Evento on_ready --------------------
@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    await bot.tree.sync(guild=guild)  # sincroniza os comandos apenas nesse servidor
    print(f"Bot online! {bot.user}")

# -------------------- Comando /ping --------------------
@bot.slash_command(name="ping", description="Pong!")
async def ping(ctx):
    await ctx.respond(f"Pong! {bot.latency * 1000:.2f}ms")

# -------------------- Comando /plano --------------------
@bot.tree.command(name="plano", description="Crie um embed personalizado para planos")
@discord.app_commands.guilds(discord.Object(id=GUILD_ID))
async def plano(interaction: discord.Interaction):
    await interaction.response.send_modal(PlanoModal())

# -------------------- Rodar Bot --------------------
bot.run(os.getenv("TOKEN"))

