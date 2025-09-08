import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# -------------------- Modal para /plano --------------------
class PlanoModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Criar Embed do Plano")

        self.add_item(discord.ui.InputText(label="Título (opcional)", placeholder="Digite o título do embed", required=False))
        self.add_item(discord.ui.InputText(label="Descrição (opcional)", placeholder="Digite a descrição", style=discord.InputTextStyle.paragraph, required=False))
        self.add_item(discord.ui.InputText(label="Campos (use | para separar) (opcional)", placeholder="Ex: Nome:Valor | Nome:Valor", required=False))
        self.add_item(discord.ui.InputText(label="Rodapé (opcional)", placeholder="Digite o rodapé", required=False))
        self.add_item(discord.ui.InputText(label="Imagem (URL opcional)", placeholder="Ex: https://link-da-imagem.com", required=False))

    async def callback(self, interaction: discord.Interaction):
        titulo = self.children[0].value or ""
        descricao = self.children[1].value or ""
        campos = self.children[2].value or ""
        rodape = self.children[3].value or ""
        imagem = self.children[4].value or ""

        # Cor padrão = preto
        cor = 0x000000

        embed = discord.Embed(title=titulo if titulo else " ", description=descricao if descricao else " ", color=cor)

        if campos:
            for campo in campos.split("|"):
                if ":" in campo:
                    nome, valor = campo.split(":", 1)
                    embed.add_field(name=nome.strip(), value=valor.strip(), inline=False)

        if rodape:
            embed.set_footer(text=rodape)

        if imagem:
            embed.set_image(url=imagem)

        await interaction.response.send_message(embed=embed, ephemeral=False)

# -------------------- Evento on_ready --------------------
@bot.event
async def on_ready():
    print(f"Bot online! {bot.user}")

# -------------------- Comando /ping --------------------
@bot.slash_command(name="ping", description="Pong!")
async def ping(ctx):
    await ctx.respond(f"Pong! {bot.latency * 1000:.2f}ms")

# -------------------- Comando /plano --------------------
@bot.slash_command(name="plano", description="Crie um embed personalizado para planos")
async def plano(ctx):
    await ctx.interaction.response.send_modal(PlanoModal())
    await ctx.delete()  # 🔹 Deleta a mensagem do comando para não mostrar "Felipe usou /plano"

# -------------------- Rodar Bot --------------------
bot.run(os.getenv("TOKEN"))

