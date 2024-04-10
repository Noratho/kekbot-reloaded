
import json
import discord
import os
import random
import globetrotters
from dotenv import load_dotenv
from discord.ext import commands

globetrotters_members = globetrotters.load_data()

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

async def failed_command(ctx):
    await ctx.send(file=discord.File('images/minijdjoker.png'))


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
        await message.channel.send(file=discord.File('images/jdjoker.png'))
        return

@bot.command(name='8ball')
async def eightball(ctx):
    response = random.choice(eightball_answers) 
    await ctx.send(response)

@bot.command(name='roll')
async def roll(ctx, *args):
    if (len(args) == 0):
        await ctx.send("Usage: ~roll d# [+/-#]")
        return

    results = []
    can_do_modifier = False;
    running_modifier = False;
    
    
    for s in args:
        
        if (len(s) > 1 and (s[0] == 'd' or s[0] == 'D')):
            s = s[1:]
        elif (len(s) > 1 and (s[0] == '+' or s[0] == '-')):
            running_modifier = True;
        
        if not running_modifier:
            try:
                die = int(s)
            except:
                await ctx.send("Usage: ``~roll d# [+/-#]``")
                return;
            if die < 1:
                await ctx.send("Error: die size must be positive\nUsage: ``~roll d# [+/-#]``")
                return;
            results.append(1 + int(die*random.random()))
            can_do_modifier = True
        
        else:
            if not can_do_modifier:
                await ctx.send("Error: modifier must be preceded by die\nUsage: ``~roll d# [+/-#]``")
                return
            try:
                mod = int(s)
            except:
                await ctx.send("Usage: ``~roll d# [+/-#]``")
                return
            results[len(results)-1] += mod
            can_do_modifier = False
            running_modifier = False


    response = ctx.author.display_name + "'s result:"
    for i in results:
        response += " " + str(i)
    
    await ctx.send(response)

@bot.command()
async def pick(ctx, *args):
    choices = ' '.join(args)
    response = random.choice(choices.split(","))
    await ctx.send(response)

@bot.command()
async def test_giveuserID(ctx):
    await ctx.send(ctx.author.id);


# TODO: split off globetrotters subfunctions into separate methods for readability
@bot.command(name='globetrotters')
async def globetrotters_split(ctx, *args):

    # set up user info
    authorid = str(ctx.author.id)
    if (authorid not in globetrotters_members.keys()):
        globetrotters_members[authorid] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # default roll
    if (len(args) == 0 or (len(args) == 1 and args[0] == "roll")):
        await globetrotters.roll(ctx)

    # filtered roll
    elif (args[0] == "roll"):
        await globetrotters.filtered_roll(ctx, args)

    # add a win to a region
    elif (args[0] == "add" or args[0] == "addwin"):
        await globetrotters.add_win(ctx, args)

    # set a win count for a region
    elif (args[0] == "set" or args[0] == "setwins"):
        await globetrotters.set_wins(ctx, args)

    # shows collated stats for all or one region
    elif (args[0] == "stats"):
        await globetrotters.show_stats(ctx, args)
        
    # manual pick
    else:
        await globetrotters.show_region(ctx, args)


@bot.command(name='numberfrom')
async def numberbetween(ctx, *args):
    if (not args[0].isdigit() or not args[1].isdigit()):
        await ctx.send(file=discord.File('images/minijdjoker.png'))
        return

    num1 = int(args[0])
    num2 = int(args[1])
    # print(num1, num2)
    if num1 >= num2:
        # failed_command(ctx)
        await ctx.send(file=discord.File('images/minijdjoker.png'))
        return

    i = random.randrange(num1, num2)
    await ctx.send(i)


bot.run(token)








