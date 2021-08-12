import os
import discord
from dotenv import load_dotenv
import random
from datetime import datetime
import pytz

import repostThisMouse as rtm
import heypat as hp

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


# For saying funny things
def convert(string):
    r = list(string.split(" "))
    return r


def splitLetters(string):
    return ([i for item in string for i in item.split()])


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # shut down
    if (message.author.id == 228379182369996801 and
            message.content == "go away"):
        await message.channel.send("simp")
        await client.close()

    # say something funny
    if (message.author.bot is False and
            message.channel.id != 480600076729712650):
        # 1/25 chance to trigger
        rng = random.randint(1, 50)
        if rng == 14:

            # Choose funny to do to sentence
            rng2 = random.randint(1, 6)

            # what u say
            if rng2 == 1:
                finalMessage = 'what'

            # Removes some words and adds yes to the end
            if rng2 == 2:
                # split sentence into words
                sentence = convert(message.content)
                for word in list(sentence):
                    rng3 = random.randint(1, 2)
                    if rng3 == 1:
                        pass
                    elif rng3 == 2:
                        sentence.remove(word)
                finalMessage = ' '.join(sentence) + ' yes'

            # shutup
            if rng2 == 3:
                finalMessage = 'shut up shut up i hate you'

            # goofy
            if rng2 == 4:
                finalMessage = '''
                shut the fuck up goofy ass nigga i will
                rock your shit if you test me one more time.
                ur always saying this and that and when i pull up ur
                not all about this and that. make up ur mind goofy ass,
                cuz me? im about that shit, i got the shooters on deck.
                wait, u hear that? yeah thats me trotting my way
                down to ur house. dont test me again nigga.
                '''

            # man
            if rng2 == 5:
                finalMessage = '>.<'

            if rng2 == 6:
                finalMessage = 'yo mom'

            await message.channel.send(finalMessage)

        else:
            pass

    # saves all messages (not from a bot) to txt file
    if (message.author.bot is False and message.content != 'go away' and
            message.content.lower() != 'hey pat' and
            len(message.content) > 7 and
            message.channel.id == 714934718155456663):
        hp.updateBrain(message.content)
        hp.updateTransitions()

    if (message.content.lower() == "hey pat" and
            message.channel.id == 317823555725295626):
        rawText = hp.rawText
        hp.updateTransitions()
        finalMessage = hp.sample_sentence(rawText, random.randint(3, 30), 1000)
        await message.channel.send(finalMessage)

    if (message.content == "hey pat get brain damage" and
            message.author.id == 228379182369996801):
        await message.channel.send('no please not my brain no')
        hp.deleteBrain()
        hp.updateTransitions()
        await message.channel.send('ooog glog haahhhh')

    if (message.content == "ping" and
            message.author.id == 228379182369996801):
        await message.channel.send('pong')


@client.event
async def on_voice_state_update(member, before, after):
    before = before.channel
    after = after.channel
    # Test channel: 317823555725295626
    # Main channel: 525446332010463262
    channel = client.get_channel(525446332010463262)
    tz = pytz.timezone('America/Los_Angeles')
    now = datetime.now(tz)
    emoji_path = "https://cdn.discordapp.com/emojis/"

    if before != after:
        # Joined channel
        if before is None and after is not None:
            embedVar = discord.Embed(
                description=(str(member) + ' joined **' + after.name + '**'),
                color=0x00ff00
            )
            embedVar.set_author(
                name='Channel Join',
                icon_url=(emoji_path + '728459179194318969.png?v=1')
            )
            embedVar.set_footer(text=(now.strftime("%m/%d/%Y %H:%M:%S PST")))

            await channel.send(embed=embedVar)
        # Left channel
        if after is None and before is not None:
            embedVar = discord.Embed(
                description=(str(member) + ' left **' + before.name + '**'),
                color=0xff0000
            )
            embedVar.set_author(
                name='Channel Left',
                icon_url=(emoji_path + '653139080820817920.png?v=1')
            )
            embedVar.set_footer(text=(now.strftime("%m/%d/%Y %H:%M:%S PST")))

            await channel.send(embed=embedVar)
        # Switched channel
        if after is not None and before is not None:
            embedVar = discord.Embed(
                description=(
                    str(member) + ' switched from **' + before.name +
                    '** to **' + after.name + "**"),
                color=0xFF7F50
            )
            embedVar.set_author(
                name='Channel Switched',
                icon_url=(emoji_path + '712882086603784233.png?v=1')
            )
            embedVar.set_footer(text=(now.strftime("%m/%d/%Y %H:%M:%S PST")))

            await channel.send(embed=embedVar)


@client.event
async def on_ready():
    game = discord.Game('fortnite')
    await client.change_presence(activity=game)
    print(f'{client.user} has connected to Discord!')

rtm.client = client
client.loop.create_task(rtm.repost_this_mouse())

client.run(TOKEN)
