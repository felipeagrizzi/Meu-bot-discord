import discord
import os
from dotenv import load_dotenv

load_dotenv()

bot = discord.Bot(intents=discord.Intents.all())

# -------------------- Modal --------------------
class PlanoModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Criar Embed do Plano")

        # Todos os campos opcionais
        self.add_item(discord.ui.InputText(label="Título", placeholder="Digite o título do embed (opcional)", required=False))
        self.add_item(discord.ui.InputText(label="Descrição", placeholder="Digite a descrição (opcional)", style=discord.InputTextStyle.long, required=False))
        self.add_item(discord.ui.InputText(label="Campos (use | para separar)", placeholder="Ex: Nome:Valor | Nome:Valor (opcional)", required=False))
        self.add_item(discord.ui.InputText(label="Rodapé", placeholder="Digite o rodapé (opcional)", required=False))
        self.add_item(discord.ui.InputText(label="Cor (hex sem #)", placeholder="Ex: FF0000 para vermelho (opcional)", required=False))
        self.add_item(discord.ui.InputText(label="URL da Imagem", placeholder="Ex: https://exemplo.com/imagem.png (opcional)", required=False))

    async def callback(self, interaction: discord.Interaction):
        try:
            titulo = self.children[0].value or ""
            descricao = self.children[1].value or ""
            campos = self.children[2].value or ""
            rodape = self.children[3].value or ""
            cor = int(self.children[4].value, 16) if self.children[4].value else 0x3498db
            imagem = self.children[5].value or ""

            embed = discord.Embed(title=titulo, description=descricao, color=cor)

            if campos:
                for campo in campos.split("|"):
                    if ":" in campo:
                        nome, valor = campo.split(":", 1)
                        embed.add_field(name=nome.strip(), value=valor.strip(), inline=False)

            if rodape:
                embed.set_footer(text=rodape)

            if imagem:
                embed.set_image(url=imagem)

            # Responde no canal sem mostrar quem enviou
            await interaction.response.send_message(embed=embed, ephemeral=False)
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
