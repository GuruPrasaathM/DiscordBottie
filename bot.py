import discord
import json
import random
from discord.ext import commands, tasks, Activity, ActivityType
from itertools import cycle
import os

bot = commands.Bot(command_prefix='.')
bot.remove_command('help')
status = cycle(['Just Chilling', 'Eating Children', 'Sleeping', 'Bombing Orphanages'])


@bot.event
async def on_ready():
    change_status.start()
    print('Bot is online.')

@bot.event
async def howmany():
    gcount=str(len(bot.guilds))
    await ctx.send(f'Currently active in {gcount} servers')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Command does not exist. Type ".help" for a list of commands.')


@bot.event
async def on_member_join(member):
    print(f'{member} has joined the server!')


@bot.event
async def on_member_remove(member):
    print(f'{member} has left the server.')


@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')


@bot.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(
        colour=discord.Colour.gold()
    )
    embed.set_author(name='Help')
    embed.add_field(name='.ping', value='Returns "Pong!", and delay of bot in milliseconds.', inline=True)
    embed.add_field(name='.8ball', value='Put in a question, and the bot will answer!', inline=True)
    embed.add_field(name='.repeat', value='Put in something to repeat, and the bot will repeat it!', inline=True)
    embed.add_field(name='.report', value='Put in a member to report, and a reason. It will be sent to the server '
                                          'owner.', inline=True)
    embed.add_field(name='.nick', value='Changes your nickname to what you want it to be.')
    embed.add_field(name='.easteregg', value='Find the secret message for a prize ;)')
    embed.add_field(name='.mods', value='you know what it is ;)', inline=True)
    embed.add_field(name='.creeper', value='Awwwww mannn', inline=True)
    embed.add_field(name='.insult', value='Put in a member, and the bot will insult them.', inline=True)
    embed.add_field(name='.randinsult', value='Put in a insult and the bot will insult a random user.', inline=True)
    embed.add_field(name='.math', value='Addition: 10 + 10. Division: 10 / 10. Multiplication: 10 * 10. Subtraction: '
                                        '10 - 10')
    embed.add_field(name='.tobinary', value='Converts a message to a list of binary letters.', inline=True)
    embed.add_field(name='.lenny', value='Put either "reg", "cry", "closed", "high", "confused", or "wink" and the bot will respond with the lenny face.', inline=True)
    embed.add_field(name='.gn', value='Says goodnight to whoever is tagged or whoever wrote the message.', inline=True)
    embed.add_field(name='.thought', value='Gives a random shower thought, straight from r/showerthoughts, or from my notes app!', inline=True)
    embed.add_field(name='.badbot', value='Give a message to send to server owner about how bad the bot is :(', inline=True)
    embed.add_field(name='.goodbot', value='Make the bot happy :D', inline=True)
    embed2 = discord.Embed(
        colour=discord.Colour.green()
    )
    embed2.set_author(name='Admin Only')
    embed2.add_field(name='.ban', value='Bans a member from the server.', inline=True)
    embed2.add_field(name='.unban', value='Unbans an already banned member from the server.', inline=True)
    embed2.add_field(name='.mute', value='Mutes a member from talking until they are unmuted.', inline=True)
    embed2.add_field(name='.unmute', value='Unmutes an already muted member.', inline=True)
    embed2.add_field(name='.kick', value='Kicks a member from the server until they join again.', inline=True)
    embed2.add_field(name='.clear', value='Clears an amount of messages.')

    await ctx.send(embed=embed)
    await ctx.send(embed=embed2)

@help.error
async def help_error(ctx, error):
    await ctx.send(f'Contact server owner about this error: {error}')

@bot.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['It is certain.',
                 'It is decidedly so.',
                 'Without a doubt.',
                 'Yes - definitely.',
                 'You may rely on it.',
                 'As I see it, yes.',
                 'Most likely.',
                 'Outlook good',
                 'Yes.',
                 'All signs point to yes.',
                 'Reply hazy, try again.',
                 'Ask again later.',
                 'Better not tell you now.',
                 'Cannot predict now.',
                 'Concentrate and ask again.',
                 "Don't count on it.",
                 'My reply is no.',
                 'My sources say no.',
                 'Outlook not so good.',
                 'Very doubtful.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


@_8ball.error
async def _8ball_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify a question.')


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify an amount of messages to delete.')


@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)


@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')


@bot.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return


@tasks.loop(seconds=60)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


@bot.command()
async def repeat(ctx, *, message):
    if message == 'i am dumb' or message == 'im dumb' or message == 'Im dumb' or message == "i'm dumb":
        await ctx.send('i know you are')
    elif message == 'I am dumb' or message == "I'm dumb" or message == "I'm stupid" or message == 'Im stupid' or message == 'I am stupid':
        await ctx.send('i know you are')
    elif message == "i'm stupid" or message == 'im stupid' or message == 'i am stupid':
        await ctx.send('i know you are')
    elif message == "i'm stoopid" or message == 'im stoopid' or message == 'i am stoopid':
        await ctx.send('No hooman, you are retarded, yu cant even spell stupid correctly')
    else:
        await ctx.send(message)


@repeat.error
async def repeat_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please put a message for me to repeat')


@bot.command()
async def report(ctx, member: discord.Member, *, reason):
    guild = ctx.guild
    channel = await guild.owner.create_dm()
    await channel.send(f'{ctx.author} Reported {member} for {reason}.')
    await ctx.send(f'Report sent to  {guild.owner}. Thank you for making this server a better place!')


@report.error
async def report_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Make sure you have a member to report, and a reason.")


@bot.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member):
    guild = ctx.guild

    for role in guild.roles:
        if role.name == "Muted":
            await member.add_roles(role)
            await ctx.send(f"{member.mention} was muted by {ctx.author.mention}")
            return


@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please put a member to mute.')


@bot.command()
async def unmute(ctx, member: discord.Member):
    guild = ctx.guild

    for role in guild.roles:
        if role.name == "Muted":
            await member.remove_roles(role)
            await ctx.send(f"{member.mention} has been unmuted by {ctx.author.mention}")
            return


@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please put a member to unmute.')


@bot.command(pass_context=True)
async def nick(ctx, *, name):
    await ctx.author.edit(nick=name)
    await ctx.send(f'Nickname was changed for {ctx.author.mention} ')


@nick.error
async def nick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Make sure you have the nickname you want to change to. You can only change your own nickname.')
    if isinstance(error, commands.TooManyArguments):
        await ctx.send('Too many arguments. Make sure you just have the nickname you want to change to. You can only '
                       'change your own nickname.')


@bot.command()
async def easteregg(ctx, *, message):
    guild = ctx.guild

    author = ctx.message.author
    channel = await author.create_dm()
    if message == 'no peeking ;)':
        await ctx.channel.purge(limit=1)
        await channel.send(f'You found the easter egg! It was "{message}".'
                           'You now have the "Easter Egg possessor" Role. Dont spoil it for others!')
        for role in guild.roles:
            if role.name == "Easter Egg possessor":
                await author.add_roles(role)
                await ctx.send(f"{author.mention} found the easter egg!")


@easteregg.error
async def easteregg_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please have a easteregg guess.')


@bot.command()
async def mods(ctx):
    await ctx.send('gay')


@bot.command()
async def tobinary(ctx, *, message):
    def string2bits(s=""):
        return [bin(ord(x))[2:].zfill(len(s)) for x in s]
    b = string2bits(message)
    await ctx.send(b)


@tobinary.error
async def binary_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please have a message that you want to convert to binary.')


@bot.command()
async def creeper(ctx):
    await ctx.send('Awwwww man')


@bot.command()
async def insult(ctx, member: discord.Member):
    guild = ctx.guild
    owner = guild.owner
    insults = [
        'is a loser',
        'likes to eat kids',
        'has no brain',
        'puts milk before cereal',
        'likes to sniff chewed up gum',
        'is a nerd',
        'has no life',
        'downloaded iFunny in 2014 and has been posting ever since',
        'committed treason in 27 countries',
        'is under fbi investigation for killing kittens',
        'is on the fbi watchlist',
        'is in prison for life for three accounts of first degree murder'
    ]
    if member == owner:
        await ctx.send(f'{owner.mention} does not deserve to be insulted because they are an awesome person.')
    else:
        await ctx.send(f'{member.mention} {random.choice(insults)}.')


@insult.error
async def insult_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Make sure you have a member to insult.')


@bot.command()
async def randinsult(ctx, *, insults):
    guild = ctx.guild
    owner = guild.owner
    user = random.choice(guild.members)
    if user == owner:
        await ctx.send(f'{owner.mention} does not deserve to be insulted because they are an awesome person.')
    else:
        await ctx.send(f'{user.mention} {insults}')


@bot.command()
async def math(ctx, a, b, c):
    if b == '+':
        await ctx.send(int(a) + int(c))
    elif b == '-':
        await ctx.send(int(a) - int(c))
    elif b == '/':
        await ctx.send(int(a) / int(c))
    elif b == '*':
        await ctx.send(int(a) * int(c))


@bot.command()
async def lenny(ctx, *, message):
    if message == "reg":
        await ctx.send('( ͡° ͜ʖ ͡°)')
    elif message == 'cry':
        await ctx.send('(☭ ͜ʖ ☭)')
    elif message == 'closed':
        await ctx.send('(ᴗ ͜ʖ ᴗ)')
    elif message == 'high':
        await ctx.send('( ͡◉ ͜ʖ ͡◉)')
    elif message == 'confused':
        await ctx.send('( ͠° ͟ʖ ͠°)')
    elif message == 'wink':
        await ctx.send('( ͡~ ͜ʖ ͡°)')
    else:
        await ctx.send('I do not have that lenny face.')


@lenny.error
async def lenny_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please put a lenny face. Ex: "reg", "cry", "closed", "high", "confused", "wink".')


@bot.command()
async def gn(ctx, member: discord.Member):
    await ctx.send(f'goodnight {member.mention}. have a good sleep')


@gn.error
async def gn_error(ctx, error):
    author = ctx.message.author
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'goodnight {author.mention}. have a good sleep')


@bot.command()
async def thought(ctx):
    thoughts = [
        "if you were invisible and closed your eyes would you see through your eyelids?",
        "baloney is just a hot dog pancake.",
        "if pinocchio told everyone that his nose grew when he was telling the truth, everyone would believe him.",
        "dying of old age is dying of not dying.",
        "do deaf people talk in their sleep?",
        "at some point in history some random guy discovered that melting sand in a certain way made blind people see again.",
        "darth vader is so famous that people recognize him by his breathing.",
        "woodpeckers are deadly to pinocchio.",
        "do crabs think we walk sideways?",
        "vampires drink blood because it has vitamin D, and they can't get vitamin D from the sun.",
        "if you fall off a high enough cliff you will be falling for the rest of your life.",
        "if you punch yourself and it hurts, are you too strong, or too weak?",
        "home depot and ikea hold hundreds of houses inside, they are just unassembled.",
        "every word in every language started out as just gibberish until someone came along and convinced everyone that what they said was a read word.",
        "if we could read each other's minds it would just create a loop.",
        "scooby doo movies are great because you know the dog isn't going to die.",
        "muffins are to cupcakes as smoothies are to milkshakes.",
        "if a centaur broke it's leg, would it be killed like a regular horse?",
        "you spend your entire life gathering guests for your funeral.",
        "what does it smell like underwater?",
        "if two people live in the same country, their driveways are connected.",
        "if you are an only child orphan, every bag of  chips you eat is family sized.",
        "your stomach is always trying to kill you - feeding it makes it stop.",
        "the worlds second best loser is actually the worlds best loser, and it creates a loop.",
        "lol is the most accepted lie.",
        "gravestones are participation awards.",
        "if you sit on your voodoo doll, you can never get up.",
        "socks are always a foot long.",
        "lego people live in houses of their own flesh.",
        "most people will die with a negative k/d.",
        "people with ADHD are just constantly doing side quests over the main story.",
        "aliens invaded the moon on july 20th, 1969.",
        "the object of golf is to play the least golf.",
        "PC's freeze when they overheat.",
        "memes are just inside jokes you spend with complete strangers.",
        "beef jerky is just cow raisins.",
        "the milk in a gallon of milk could be from hundreds of different cows."
    ]
    await ctx.send(random.choice(thoughts))


@bot.command()
async def badbot(ctx, *, issue):
    guild = ctx.message.guild
    author = ctx.message.author
    channel = await guild.owner.create_dm()
    await channel.send(f'''{author.mention} reported me for "{issue}",
   I am sorrie about this, the same has been reported to the bot dev''')
    await ctx.send(f"Sorrie, I'll report this issue to owner, Your issue: {issue}")


@badbot.error
async def badbot_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please have an issue that you have with me.')


@bot.command()
async def goodbot(ctx):
    author = ctx.message.author
    await ctx.send(f'Thank you {author.mention}. You made me happie :D')

@bot.command()
async def guru(ctx):
    await ctx.send(f'Greatest Hooman to ever exist')

bot.run(os.environ['DISCORD_TOKEN'])
