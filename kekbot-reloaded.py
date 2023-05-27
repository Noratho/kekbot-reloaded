
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

globetrotters_display_names = ["Bandle City", "Bilgewater", "Frelijord", "Ionia", 
                    "Ixtal", "Noxus", "Piltover", "The Shadow Isles", 
                    "Shurima", "Targon", "The Void", "Zaun", "Demacia"]

globetrotters_aliases = [
                    ["bandle", "bandlecity", "yordle", "yordles", "5under5", "fiveunderfive", "5under5'"],
                    ["bilgewater", "yarhar", "yarharhar", "allhandsondeck"],
                    ["frelijord", "iceicebaby"],
                    ["ionia", "ionian", "wuju", "everybodywaswujufighting"],
                    ["ixtal", "elemental", "elementalmydearwatson", "elemental,mydearwatson"],
                    ["noxus", "noxian", "strengthaboveall"],
                    ["piltover", "hextech", "calculated"],
                    ["theshadowisles", "shadowisles", "ruination", "harrowing", "spookyscaryskeletons"],
                    ["shurima", "thesundiscneversets"],
                    ["targon", "mounttargon", "peakperformance"],
                    ["void", "thevoid", "inhumanscreechingsounds", "(inhumanscreechingsounds)"],
                    ["zaun", "zaunite", "chemtech", "chemtechcomrades"],
                    ["demacia", "demacian", "fordemacia"]
                ]

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
async def globetrotters(ctx, *args):
    
    # default roll
    if (len(args) == 0 or args == ["roll"]):
        i = random.randrange(0, 12)
        await ctx.send(globetrotters_display_names[i])
        await ctx.send(file=discord.File("globetrotter_images/" +globetrotters_images[i]))


    # add a win to a region [TODO]
    elif (args[0] == "add" or args[0] == "addto"):

        # dummy text
        await ctx.send("Coming soon™")
        return
    
        if (len(args) < 2):
            await ctx.send("Missing arguments. Usage: ~globetrotters add [region name]")
            return

        # get name
        args.pop(0);
        name = ''.join(args).lower();

        # get wins
        for i in range(len(globetrotters_aliases)):
            if (name in globetrotters_aliases[i]):
                # add a win
                return

        # if nothing found...
        await ctx.send("No such area exists. Usage: ~globetrotters add [region name]")
        

    # set a win count for a region [TODO]
    elif (args[0] == "set"):

        # dummy text
        await ctx.send("Coming soon™")
        return
        
        if (len(args) < 3):
            await ctx.send("Missing arguments. Usage: ~globetrotters set [region name] [wins]")
            return
        
        count = args[len(args)-1]
        if (not count.isdigit()):
            await ctx.send("Can't set your win count to a non-integer. Usage: ~globetrotters set [region] [wins]")
            return
        count = int(count)

        # get name
        args.pop(0);
        args.pop(len(args)-1)
        name = ''.join(args).lower();

        # get wins
        for i in range(len(globetrotters_aliases)):
            if (name in globetrotters_aliases[i]):
                # set the wins
                return

        # if nothing found...
        await ctx.send("No such area exists. Usage: ~globetrotters set [region name] [wins]")


    # shows collated stats for all or one region [TODO]
    elif (args[0] == "stats"):

        # dummy text
        await ctx.send("Coming soon™")
        return
    
        args.pop(0);

        if (len(args) == 0):
            return

        else:
            name = ''.join(args).lower();
            found = False;

    
    # manual pick
    else:
        name = ''.join(args).lower();
        
        for i in range(len(globetrotters_aliases)):
            if (name in globetrotters_aliases[i]):
                await ctx.send(globetrotters_display_names[i])
                await ctx.send(file=discord.File("globetrotter_images/" +globetrotters_images[i]))
                return

        # if nothing found...
        await ctx.send("No such area exists")
    

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








