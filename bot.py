import os
from config import token1, api_key1, secret_key1
import discord
from discord.ext import commands
from main import FusionBrainAPI

# Initialization
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
       
# Message Handling (Image)       
@bot.event
async def on_message(message):
       if message.author == bot.user:
              return
    
       prompt = message.content
       api = FusionBrainAPI(
              'https://api-key.fusionbrain.ai/',
              api_key1,
              secret_key1
       )

       pipeline_id = api.get_pipeline()
       uuid = api.generate(prompt, pipeline_id, images=1)
       files = api.check_generation(uuid)
       filepath = "gen_img.png"
       api.sv_img(files, filepath)

       # File Delivery
       with open(filepath, "rb") as f:
              file = discord.File(f)
       await message.channel.send(file=discord.File(f, filepath))
       
       os.remove(filepath)
    
# Connection
bot.run(token=token1)