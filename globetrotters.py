import os
import random
import json
import discord
import utils


globetrotters_display_names = ["Bandle City", "Bilgewater", "Frelijord", "Ionia",
                               "Ixtal", "Noxus", "Piltover", "The Shadow Isles",
                               "Shurima", "Targon", "The Void", "Zaun", "Demacia"]

globetrotters_aliases = [
    ["bandle", "bandlecity", "yordle", "yordles",
        "5under5", "fiveunderfive", "5under5'"],
    ["bilgewater", "yarhar", "yarharhar", "allhandsondeck"],
    ["frelijord", "frelijordian", "iceicebaby"],
    ["ionia", "ionian", "wuju", "everybodywaswujufighting"],
    ["ixtal", "ixtali" "elemental",
     "elementalmydearwatson", "elemental,mydearwatson"],
    ["noxus", "noxian", "strengthaboveall"],
    ["piltover", "piltovan", "hextech", "calculated"],
    ["theshadowisles", "shadowisles", "ruination",
     "harrowing", "spookyscaryskeletons"],
    ["shurima", "shuriman", "thesundiscneversets"],
    ["targon", "mounttargon", "targonian", "peakperformance"],
    ["void", "thevoid", "inhumanscreechingsounds",
                        "(inhumanscreechingsounds)"],
    ["zaun", "zaunite", "chemtech", "chemtechcomrades"],
    ["demacia", "demacian", "fordemacia", "fordemacia!"]
]

globetrotters_images = ["1yordles.png", "2bilgewater.png", "3frelijord.png", "4ionia.png",
                        "5ixtal.png", "6noxus.png", "7piltover.png", "8shadow_isles.png",
                        "9shurima.png", "10trgon.png", "11vod.png", "12zun.png", "13demc.png"]


def load_data():
    globetrotters_members = {}
    globetrotters_file = 'data/globetrotters.json'
    if os.path.isfile(globetrotters_file):
        with open(globetrotters_file, "r") as read_file:
            globetrotters_members = json.load(read_file)
    return globetrotters_members


async def roll(ctx):
    i = random.randrange(0, 12)
    await ctx.send(globetrotters_display_names[i])
    await ctx.send(file=discord.File("images/globetrotter/" + globetrotters_images[i]))


async def filtered_roll(ctx, args):
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
    await ctx.send(file=discord.File("images/globetrotter/" + globetrotters_images[i]))


async def add_win(ctx, args):
    if (len(args) < 2):
        await ctx.send("Missing arguments. Usage: ``~globetrotters add [region name]``")
        return

    authorid = str(ctx.author.id)

    # get name
    argslist = utils.generate_argslist(args)
    argslist.pop(0)
    name = ''.join(argslist).lower()

    # add a win
    for i in range(len(globetrotters_aliases)):
        if (name in globetrotters_aliases[i]):
            count = globetrotters_members[authorid][i] + 1
            globetrotters_members[authorid][i] = count

            with open(globetrotters_file, "w") as read_file:
                json.dump(globetrotters_members, read_file)

            await ctx.send("Congrats! You now have " + str(globetrotters_members[authorid][i]) + (" wins with " if count != 1 else " win with ") + globetrotters_display_names[i] + ".")
            return

    # if nothing found...
    await ctx.send("No such region exists. Usage: ``~globetrotters add [region name]``")


async def set_wins(ctx, args):
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
    argslist = utils.generate_argslist(args)
    argslist.pop(0)
    argslist.pop(len(argslist)-1)
    name = ''.join(argslist).lower()

    # get wins
    for i in range(len(globetrotters_aliases)):
        if (name in globetrotters_aliases[i]):
            globetrotters_members[authorid][i] = count

            with open(globetrotters_file, "w") as read_file:
                json.dump(globetrotters_members, read_file)

            await ctx.send("Set " + globetrotters_display_names[i] + " wins to " + str(globetrotters_members[authorid][i]) + ".")
            return

    # if nothing found...
    await ctx.send("No such region exists. Usage: ``~globetrotters set [region name] [wins]``")


async def show_stats(ctx, args):
    authorid = str(ctx.author.id)

    message = "**Globetrotters Records for " + ctx.author.display_name + "**\n"

    if (len(args) == 1):
        for i in range(len(globetrotters_aliases)):
            count = globetrotters_members[authorid][i]
            message = message + "*" + globetrotters_display_names[i] + ":* " + str(
                count) + (" wins" if count != 1 else " win") + "\n"
        await ctx.send(message)

    else:
        argslist = utils.generate_argslist(args)
        argslist.pop(0)
        name = ''.join(argslist).lower()

        for i in range(len(globetrotters_aliases)):
            if (name in globetrotters_aliases[i]):
                count = globetrotters_members[authorid][i]
                message = message + "*" + \
                    globetrotters_display_names[i] + ":* " + \
                    str(count) + (" wins" if count != 1 else " win")
                await ctx.send(message)
                return

        # if nothing found...
        await ctx.send("No such region exists.")


async def show_region(ctx, args):
    name = ''.join(args).lower()

    for i in range(len(globetrotters_aliases)):
        if (name in globetrotters_aliases[i]):
            await ctx.send(globetrotters_display_names[i])
            await ctx.send(file=discord.File("images/globetrotter/" + globetrotters_images[i]))
            return

    # if nothing found...
    await ctx.send("No such region exists.")
