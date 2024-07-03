import asyncio
import discord
import os
from discord import Intents
from keep_alive import keep_alive
import emails

intents = Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)

# Cargos
COORDENADOR_ROLE = "Coordenador"
ALUNO_ROLE = "Aluno"
PROFESSOR_ROLE = "Professor"
DEV_ROLE = "Dev"
EGRESSO_ROLE = "Egresso"
PRETENDENTE_ROLE = "Pretendente"

# Canais
BEM_VINDO_CHANNEL = "bem-vindo"
REGRAS_CHANNEL = "regras"
AVISOS_CHANNEL = "avisos-da-coordenacao"
OPORTUNIDADES_EMPREGO_CHANNEL = "oportunidades-de-emprego"
OPORTUNIDADES_INTERNAS_CHANNEL = "oportunidades-internas"
DUVIDAS_CHANNEL = "duvidas"
OFF_TOPIC_CHANNEL = "off-topic"
PROFESSORES_CHANNEL = "professores"

# Autenticação
def authenticate(user_email):
    if user_email in emails.alunos:
        return ALUNO_ROLE
    elif user_email in emails.professores:
        return PROFESSOR_ROLE
    return None

@client.event
async def on_ready():
    print(f'{client.user} Está Online e roteando!')
    guild = client.guilds[0]
    print(f'Conectado ao servidor: {guild.name}')

    # Cria os cargos se eles não existirem
    roles = [COORDENADOR_ROLE, ALUNO_ROLE, PROFESSOR_ROLE, DEV_ROLE, EGRESSO_ROLE, PRETENDENTE_ROLE]
    for role in roles:
        if not discord.utils.get(guild.roles, name=role):
            await guild.create_role(name=role)
            print(f'Cargo {role} criado.')

    # Verifica se a categoria existe, se não, cria a categoria
    category = discord.utils.get(guild.categories, name='Engenharia de Computação')
    if not category:
        category = await guild.create_category('Engenharia de Computação')
        print('Categoria Engenharia de Computação criada.')

    # Cria os canais se eles não existirem
    channels = [BEM_VINDO_CHANNEL, REGRAS_CHANNEL, AVISOS_CHANNEL, OPORTUNIDADES_EMPREGO_CHANNEL,
                OPORTUNIDADES_INTERNAS_CHANNEL, DUVIDAS_CHANNEL, OFF_TOPIC_CHANNEL, PROFESSORES_CHANNEL]
    for channel in channels:
        if not discord.utils.get(guild.channels, name=channel):
            await guild.create_text_channel(name=channel, category=category)
            print(f'Canal {channel} criado.')

    # Exclui a categoria "canais de texto" se ela existir
    text_category = discord.utils.get(guild.categories, name='canais de texto')
    if text_category:
        for channel in text_category.channels:
            await channel.delete()
            print(f'Canal {channel.name} excluído.')
        await text_category.delete()
        print('Categoria "canais de texto" excluída.')

@client.event
async def on_member_join(member: discord.Member):
    role = discord.utils.get(member.guild.roles, name=PRETENDENTE_ROLE)
    await member.add_roles(role)

    await member.send(f'Bem-vindo(a) {member.name}! Para se autenticar, por favor, informe o seu email institucional:')

    def check_author(m):
        return m.author == member

    max_attempts = 5
    for i in range(max_attempts):
        try:
            message = await client.wait_for('message', check=check_author, timeout=5000)
            user_email = message.content

            role_name = authenticate(user_email)
            if role_name:
                role = discord.utils.get(member.guild.roles, name=role_name)
                await member.add_roles(role)
                await member.remove_roles(discord.utils.get(member.guild.roles, name=PRETENDENTE_ROLE))

                channel = discord.utils.get(member.guild.text_channels, name=BEM_VINDO_CHANNEL)
                await channel.send(f'Bem-vindo(a) {member.name}!')
                await member.send(f'{member.name}, você foi autenticado com sucesso!')
                break
            else:
                await member.send(f'{member.name}, seu email não está na base de dados. Por favor, tente novamente.')
        except asyncio.TimeoutError:
            await member.send(f'{member.name}, você excedeu o tempo limite para autenticação. Você foi banido do servidor.')
            await member.ban(reason="Tempo limite excedido")
            await asyncio.sleep(20)
            await member.guild.unban(member)
            return
    else:
        await member.send(f'{member.name}, você excedeu a quantidade de tentativas para autenticação. Você foi banido do servidor.')
        await asyncio.sleep(20)
        await member.ban(reason="Quantidade de tentativas excedida")

my_secret = os.environ['DISCORD_TOKEN']
keep_alive()
client.run(my_secret)
