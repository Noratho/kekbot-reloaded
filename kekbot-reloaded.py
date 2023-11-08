
import json
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


globetrotters_file = 'data/globetrotters.json'
if os.path.isfile(globetrotters_file):
    with open(globetrotters_file, "r") as read_file:
        globetrotters_members = json.load(read_file)
else:
    globetrotters_members = {}

globetrotters_display_names = ["Bandle City", "Bilgewater", "Frelijord", "Ionia", 
                    "Ixtal", "Noxus", "Piltover", "The Shadow Isles", 
                    "Shurima", "Targon", "The Void", "Zaun", "Demacia"]

globetrotters_aliases = [
                    ["bandle", "bandlecity", "yordle", "yordles", "5under5", "fiveunderfive", "5under5'"],
                    ["bilgewater", "yarhar", "yarharhar", "allhandsondeck"],
                    ["frelijord", "frelijordian", "iceicebaby"],
                    ["ionia", "ionian", "wuju", "everybodywaswujufighting"],
                    ["ixtal", "ixtali" "elemental", "elementalmydearwatson", "elemental,mydearwatson"],
                    ["noxus", "noxian", "strengthaboveall"],
                    ["piltover", "piltovan", "hextech", "calculated"],
                    ["theshadowisles", "shadowisles", "ruination", "harrowing", "spookyscaryskeletons"],
                    ["shurima", "shuriman", "thesundiscneversets"],
                    ["targon", "mounttargon", "targonian", "peakperformance"],
                    ["void", "thevoid", "inhumanscreechingsounds", "(inhumanscreechingsounds)"],
                    ["zaun", "zaunite", "chemtech", "chemtechcomrades"],
                    ["demacia", "demacian", "fordemacia", "fordemacia!"]
                ]

globetrotters_images = ["1yordles.png", "2bilgewater.png", "3frelijord.png", "4ionia.png", 
                    "5ixtal.png", "6noxus.png", "7piltover.png", "8shadow_isles.png", 
                    "9shurima.png", "10trgon.png", "11vod.png", "12zun.png", "13demc.png"]



bot = commands.Bot(command_prefix='~', intents=defIntents)

def generate_argslist(args):
    argslist = [];
    for a in args:
        argslist.append(a)
    return argslist

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
@bot.command()
async def globetrotters(ctx, *args):

    # set up user info
    authorid = str(ctx.author.id)
    if (authorid not in globetrotters_members.keys()):
        globetrotters_members[authorid] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # default roll
    if (len(args) == 0 or (len(args) == 1 and args[0] == "roll")):
        await globetrotters_roll(ctx)

    # filtered roll
    elif (args[0] == "roll"):
        await globetrotters_filtered_roll(ctx, args)

    # add a win to a region
    elif (args[0] == "add" or args[0] == "addwin"):
        await globetrotters_add_win(ctx, args)

    # set a win count for a region
    elif (args[0] == "set" or args[0] == "setwins"):
        await globetrotters_set_wins(ctx, args)

    # shows collated stats for all or one region
    elif (args[0] == "stats"):
        await globetrotters_show_stats(ctx, args)
        
    # manual pick
    else:
        await globetrotters_show_region(ctx, args)


async def globetrotters_roll(ctx):
    i = random.randrange(0, 12)
    await ctx.send(globetrotters_display_names[i])
    await ctx.send(file=discord.File("images/globetrotter/" +globetrotters_images[i]))


async def globetrotters_filtered_roll(ctx, args):
    maxwins = args[1]
    if (not maxwins.isdigit()):
        await ctx.send("Can't use a non-integer to filter rolls. Usage: ``~globetrotters roll [maxwins]``")
        return
    maxwins = int(maxwins)

    authorid = str(ctx.author.id)

    filteredindices = []
    for i in range(len(globetrotters_aliases)):
        if (globetrotters_members[authorid][i] <= maxwins):
            filteredindices.append(i)
    if (len(filteredindices) <= 0):
        await ctx.send("Maximum win count is too low. Use ``~globetrotters stats`` to check your current win counts.")
        return
        
    i = filteredindices[random.randrange(0, len(filteredindices))]
    await ctx.send(globetrotters_display_names[i])
    await ctx.send(file=discord.File("images/globetrotter/" +globetrotters_images[i]))


async def globetrotters_add_win(ctx, args):
    if (len(args) < 2):
        await ctx.send("Missing arguments. Usage: ``~globetrotters add [region name]``")
        return

    authorid = str(ctx.author.id)
    
    # get name
    argslist = generate_argslist(args)
    argslist.pop(0);
    name = ''.join(argslist).lower();

    # add a win
    for i in range(len(globetrotters_aliases)):
        if (name in globetrotters_aliases[i]):
            count = globetrotters_members[authorid][i] + 1
            globetrotters_members[authorid][i] = count
            
            with open(globetrotters_file, "w") as read_file:
                json.dump(globetrotters_members, read_file);
            
            await ctx.send("Congrats! You now have " + str(globetrotters_members[authorid][i]) + (" wins with " if count != 1 else " win with ") + globetrotters_display_names[i] + ".")
            return

    # if nothing found...
    await ctx.send("No such region exists. Usage: ``~globetrotters add [region name]``")


async def globetrotters_set_wins(ctx, args):
    if (len(args) < 3):
        await ctx.send("Missing arguments. Usage: ``~globetrotters set [region name] [wins]``")
        return
    
    count = args[len(args)-1]
    if (not count.isdigit()):
        await ctx.send("Can't set your win count to a non-integer. Usage: ``~globetrotters set [region] [wins]``")
        return
    count = int(count)

    authorid = str(ctx.author.id)

    # get name
    argslist = generate_argslist(args)
    argslist.pop(0);
    argslist.pop(len(argslist)-1)
    name = ''.join(argslist).lower();

    # get wins
    for i in range(len(globetrotters_aliases)):
        if (name in globetrotters_aliases[i]):
            globetrotters_members[authorid][i] = count

            with open(globetrotters_file, "w") as read_file:
                json.dump(globetrotters_members, read_file);
            
            await ctx.send("Set " + globetrotters_display_names[i] + " wins to " + str(globetrotters_members[authorid][i]) + ".")
            return

    # if nothing found...
    await ctx.send("No such region exists. Usage: ``~globetrotters set [region name] [wins]``")


async def globetrotters_show_stats(ctx, args):
    authorid = str(ctx.author.id)
    
    message = "**Globetrotters Records for " + ctx.author.display_name + "**\n"
    
    if (len(args) == 1):
        for i in range(len(globetrotters_aliases)):
            count = globetrotters_members[authorid][i]
            message = message + "*" + globetrotters_display_names[i] + ":* " + str(count) + (" wins" if count != 1 else " win") + "\n"
        await ctx.send(message)

    else:
        argslist = generate_argslist(args)
        argslist.pop(0);
        name = ''.join(argslist).lower();

        for i in range(len(globetrotters_aliases)):
            if (name in globetrotters_aliases[i]):
                count = globetrotters_members[authorid][i]
                message = message + "*" + globetrotters_display_names[i] + ":* " + str(count) + (" wins" if count != 1 else " win")
                await ctx.send(message)
                return

        # if nothing found...
        await ctx.send("No such region exists.")


async def globetrotters_show_region(ctx, args):
    name = ''.join(args).lower();
    
    for i in range(len(globetrotters_aliases)):
        if (name in globetrotters_aliases[i]):
            await ctx.send(globetrotters_display_names[i])
            await ctx.send(file=discord.File("images/globetrotter/" +globetrotters_images[i]))
            return

    # if nothing found...
    await ctx.send("No such region exists.")


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








