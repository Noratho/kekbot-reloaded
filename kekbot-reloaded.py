
import discord
import os
import random
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
  
defIntents = discord.Intents.default()
defIntents.message_content = True
token = os.getenv('TOKEN')

eightball_answers = ["It is certain", "It is decidedly so", "Without a doubt", "Yes definitely", 
                "You may rely on it", "As I see it, yes", "Most likely", "Outlook good", "Yes",
                "Signs point to yes", "Reply hazy, try again", "Ask again later", "Better not tell you now",
                "Cannot predict now", "Concentrate and ask again", "Don’t count on it", "My reply is no", 
                "My sources say no", "Outlook not so good", "Very doubtful"]


globetrotters_name = ["Bandle City", "Bilgewater", "Frelijord", "Ionia", 
                    "Ixtal", "Noxus", "Piltover", "The Shadow Isles", 
                    "Shurima", "Targon", "The Void", "Zaun", "Demacia"]

globetrotters_images = ["1yordles.png", "2bilgewater.png", "3frelijord.png", "4ionia.png", 
                    "5ixtal.png", "6noxus.png", "7piltover.png", "8shadow_isles.png", 
                    "9shurima.png", "10trgon.png", "11vod.png", "12zun.png", "13demc.png"]



bot = commands.Bot(command_prefix='~', intents=defIntents)


async def failed_command(ctx):
    await ctx.send(file=discord.File('minijdjoker.png'))


@bot.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(bot))
    global botname
    botname = "{0.user}".format(bot)
    # print(botname)


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if "major" in message.content.lower() and str(message.author) != botname:
        await message.channel.send("I don't have a major.")
        await message.channel.send(file=discord.File('jdjoker.png'))
        return

@bot.command(name='8ball')
async def eightball(ctx):
    response = random.choice(eightball_answers) 
    await ctx.send(response)


@bot.command()
async def pick(ctx, *args):
    choices = ' '.join(args)
    response = random.choice(choices.split(","))
    await ctx.send(response)


@bot.command()
async def globetrotters(ctx):
    i = random.randrange(0, 12)

    await ctx.send(globetrotters_name[i])
    await ctx.send(file=discord.File("globetrotter_images/" +globetrotters_images[i]))


@bot.command(name='numberfrom')
async def numberbetween(ctx, *args):
    if (not args[0].isdigit() or not args[1].isdigit()):
        await ctx.send(file=discord.File('minijdjoker.png'))
        return

    num1 = int(args[0])
    num2 = int(args[1])
    # print(num1, num2)
    if num1 >= num2:
        # failed_command(ctx)
        await ctx.send(file=discord.File('minijdjoker.png'))
        return

    i = random.randrange(num1, num2)
    await ctx.send(i)


bot.run(token)








