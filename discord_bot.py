import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def send_message(ctx, channel_id, message):
    channel = bot.get_channel(int(channel_id))
    await channel.send(message)


bot.run('MTE2MDYxMDA2MDMzMDg4MTA3NA.GyHQ9f.0jVHELwxq5Aj9-oTpfUay0WBEGNmSRW0tpVLjo')