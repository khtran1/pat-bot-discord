import asyncio
from time import perf_counter
import random
import nextcord

import json
import driveAuth as auth

client = None
# Test : 432011496696971274         Main: 236513266321457152
channelID = 236513266321457152

the_mouse = 874553330372861972

mouse_url = (
    "https://media.discordapp.net/attachments/"
    "236513266321457152/874515974534090782/"
    "image0.png?width=576&height=676"
)


def get_global_leaderboard():
    print('Getting the latest leaderboard from the drive...')

    filesList = auth.drive.ListFile({'q': "trashed=false"}).GetList()

    for files in filesList:
        if files['title'] == 'leaderboard.json':
            global_leaderboard = files.GetContentString("leaderboard.json")

            return global_leaderboard


def update_global_leaderboard(leaderboard_str):
    print('Updating the leaderboard...')

    filesList = auth.drive.ListFile({'q': "trashed=false"}).GetList()

    for files in filesList:
        if files['title'] == 'leaderboard.json':
            files.SetContentString(leaderboard_str)
            print('Uploading...')
            files.Upload()
            print('Uploaded new leaderboard.')
            break


async def send_leaderboard(channelID):

    channel = client.get_channel(channelID)

    embed = nextcord.Embed(title="Leaderboard", color=0xffaa00)

    embed.set_thumbnail(url=mouse_url)

    leaderboard_text = ""

    data = get_global_leaderboard()
    leaderboard = json.loads(data)

    for pos, (userid, time_score) in enumerate(leaderboard.items()):
        try:
            username = await client.fetch_user(userid)
            leaderboard_text += f"{pos+1}. {username} - {time_score} sec\n"
        except Exception as e:
            print("Error in enumerating leaderboard: ", e)
            break

    embed.add_field(
        name="who repost da mouse fastest",
        value=leaderboard_text,
        inline=True
    )

    await channel.send(embed=embed)


def format_leaderboard(leaderboard_dict):
    # Sort the dictionary by lowest times (values) first
    sorted_list = sorted(leaderboard_dict.items(), key=lambda x: x[1])
    sorted_dict = {}

    # Get only the first 5 entries
    sorted_list = sorted_list[:5]

    # Turn dictionary list back into a dict
    for i in sorted_list:
        sorted_dict[i[0]] = i[1]

    print(sorted_dict)
    return sorted_dict


def update_leaderboard(winner_dict):
    leaderboard = {}
    exists = False
    try:
        # Get leaderboard from drive as a string
        data = get_global_leaderboard()
        # Turn that string into a json dict
        leaderboard = json.loads(data)
    except Exception as e:
        print('Empty leaderboard: ', e)
        leaderboard = {}

    winnerKey = list(winner_dict.keys())[0]
    winnerValue = list(winner_dict.values())[0]

    for key, value in leaderboard.items():

        if str(winnerKey) == key:
            exists = True
            print('in leaderboard', value)
            break

    if exists:
        if float(winnerValue) <= float(value):
            print('lower!')
            # Edit json dict to update lower times
            leaderboard[str(winnerKey)] = float(winnerValue)

            # new_leaderboard string = string dump of the json leaderboard
            new_leaderboard = json.dumps(format_leaderboard(leaderboard))
        else:
            new_leaderboard = json.dumps(format_leaderboard(leaderboard))
    else:
        print('adding to leaderboard')

        leaderboard.update(winner_dict)

        new_leaderboard = json.dumps(format_leaderboard(leaderboard))

    update_global_leaderboard(new_leaderboard)


async def repost_this_mouse():
    await client.wait_until_ready()

    channel = client.get_channel(channelID)
    mouse_sticker = await client.fetch_sticker(the_mouse)

    while not client.is_closed():
        secondsTillMouse = random.randint(0, 5)
        print(f'Next mouse in {secondsTillMouse} seconds')

        await asyncio.sleep(secondsTillMouse)

        await channel.send(stickers=[mouse_sticker])

        def check(m):
            if (m.stickers):
                if (m.stickers[0].id == the_mouse and
                        m.channel == channel):

                    return True

        start = perf_counter()

        winner = await client.wait_for("message", check=check)

        end = perf_counter()

        print(f'{winner.author} reposted in {end-start:.2f} seconds')

        await channel.send(
            content=(
                f"{winner.author.mention} reposted the mouse in "
                f"{round(end-start, 2)} seconds"
                " <:whitecat:712882086603784233>"
            )
        )

        winner_dict = {}

        winner_dict[winner.author.id] = round(end-start, 2)

        update_leaderboard(winner_dict)

        await send_leaderboard(channelID)
