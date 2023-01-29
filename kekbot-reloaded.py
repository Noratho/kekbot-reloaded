
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

bot = commands.Bot(command_prefix='~', intents=defIntents)


@bot.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(bot))
    global botname
    botname = "{0.user}".format(bot)
    # print(botname)


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    # print(str(message.author), botname)
    if "major" in message.content.lower() and str(message.author) != botname:
        await message.channel.send("I don't have a major.")
        await message.channel.send(file=discord.File('jdjoker.png'))
        return

@bot.command(name='8ball')
async def eightball(ctx):
    response = random.choice(eightball_answers) \
    await ctx.send(response)


@bot.command()
async def pick(ctx, *args):
    choices = ' '.join(args)
    response = random.choice(choices.split(","))
    await ctx.send(response)


bot.run(token)








