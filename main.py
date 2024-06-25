import discord
from discord.ext import commands
import os
from mihomo import Language, MihomoAPI
from card import create_card
from utils import get_config

TOKEN = '' # place your bot token here

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None) # edit prefix here

client = MihomoAPI(Language.EN)
config = get_config()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='help')
async def help(ctx):
    await ctx.send("https://github.com/yuvlian/railgen/blob/main/README.md")

@bot.command(name='railgen')
async def railgen(ctx, uid: int, char_index: int, image_url: str = None):
    try:
        data = await client.fetch_user(uid, replace_icon_name_with_url=True)
        await ctx.send(f"Fetching user data...")
        if char_index == 0:
            for i, ch in enumerate(data.characters):
                await ctx.send(f"Generating card for {uid}, {ch.name}...")
                img_url = image_url if image_url else await ask_for_image_url(ctx, ch.name)
                img = create_card(data, i, img_url)
                save_card(img, uid, ch.name)
                await ctx.send(f"Card generation for {ch.name} complete! Sending the card...")
                await ctx.send(file=discord.File(os.path.join(config["cardsPath"], str(uid), f"{ch.name}.png")))
                await delete_card(ctx, uid, ch.name)
        else:
            selected_char = data.characters[char_index - 1]
            await ctx.send(f"Generating card for {uid}, {selected_char.name}...")
            img_url = image_url if image_url else await ask_for_image_url(ctx, selected_char.name)
            img = create_card(data, char_index - 1, img_url)
            save_card(img, uid, selected_char.name)
            await ctx.send(file=discord.File(os.path.join(config["cardsPath"], str(uid), f"{selected_char.name}.png")))
            await delete_card(ctx, uid, selected_char.name)

    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

@railgen.error
async def railgen_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Invalid arguments. Please use the correct format: !railgen <uid:int> <char_index:int> <image_url:str|none>")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing arguments. Please use the correct format: !railgen <uid:int> <char_index:int> <image_url:str|none>")

@bot.command(name='charlist')
async def charlist(ctx, uid: int):
    try:
        data = await client.fetch_user(uid, replace_icon_name_with_url=True)
        char_list = "\n".join([f"[{i + 1}] {ch.name}" for i, ch in enumerate(data.characters)])
        await ctx.send(f"Character List for {uid}:\n```{char_list}```")
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

@charlist.error
async def railgen_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Invalid arguments. Please use the correct format: !charlist <uid:int>")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing arguments. Please use the correct format: !charlist <uid:int>")

async def ask_for_image_url(ctx, character_name):
    await ctx.send(f"Enter the URL of character image for {character_name}'s card (or type 'n' to skip): ")
    msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    return msg.content if msg.content.lower().strip() != 'n' else None

def save_card(img, uid, char_name):
    pth = os.path.join(config["cardsPath"], str(uid))
    os.makedirs(pth, exist_ok=True)
    img.save(os.path.join(pth, f"{char_name}.png"))

async def delete_card(ctx, uid, char_name):
    try:
        os.remove(os.path.join(config["cardsPath"], str(uid), f"{char_name}.png"))
    except Exception as e:
        await ctx.send(f"Failed to delete image: {str(e)}")

bot.run(TOKEN)
