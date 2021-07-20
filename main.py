Skip to content
Search or jump to…

Pull requests
Issues
Marketplace
Explore
 
@patrikvince 
import os
# import time

import discord
# import schedule
import youtube_dl
from discord.ext import commands

# file reading
with open("Keys.txt") as f:
    auth = f.readlines()
auth = [x.strip() for x in auth]

bot = commands.Bot(command_prefix="!!")
INFO_CHANNEL_ID = int(auth[0])


# commands

@bot.command()
async def szia_uram(ctx):
    await ctx.send("Szia uram!")


@bot.command()
async def gyrosos_kard(ctx):
    await ctx.send("Ez nem tőr, ez egy gyrosos kard!")
    await play(ctx, "https://www.youtube.com/watch?v=doA_m4azblU")


@bot.command()
async def trinyo(ctx):
    await ctx.send("Ez a trinyó testvérem!")
    await play(ctx, "https://www.youtube.com/watch?v=By8OY6WTVE8")


@bot.command()
async def polgarmester(ctx):
    await play(ctx, "https://www.youtube.com/watch?v=99WgR24jWcw")


@bot.command()
async def kamuroli(ctx):
    await play(ctx, "https://www.youtube.com/watch?v=zBcKcW0K8oQ")


@bot.command()
async def aldas(ctx):
    await ctx.send("HOLY HOLY HOLY HOLY")
    await play(ctx, "https://www.youtube.com/watch?v=PnbvRQBMQHE")

@bot.command()
async def remix(ctx):
    await play(ctx, "https://www.youtube.com/watch?v=tF_9ASONj1M")

@bot.command()
async def parancsok(ctx):
    await ctx.send(
        "!!szia_uram, !!gyrosos_kard, !!trinyo, !!polgarmester, !!kamuroli, !!aldas, !!stat, !!play, "
        "!!pause, !!resume, !!stop, !!leave")


# Song

@bot.command()
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voice_channel = discord.utils.get(ctx.guild.voice_channels, name='Discord_Room_Name')
    await voice_channel.connect()
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@bot.command()
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()

"""
# Auto play not working yet
def autoplay(url: str):
    play(url)


schedule.every().day.at("12:00").do(autoplay, url="https://www.youtube.com/watch?v=RifAjo05uLI")
schedule.every().day.at("17:00").do(autoplay, url="https://www.youtube.com/watch?v=1LrY5xfS49o")
schedule.every().day.at("00:00").do(autoplay, url="https://www.youtube.com/watch?v=JHG0S75PrD0")

while True:
    schedule.run_pending()
    time.sleep(1)
"""

# RIOT API

watcher = LolWatcher(auth[2])

@bot.command()
async def stat(ctx, summoner_name):
    try:
        summoner = watcher.summoner.by_name('eun1', summoner_name)
        stats = watcher.league.by_summoner('eun1', summoner['id'])
        print(stats)
        try:
            tier = stats[0]['tier']
            rank = stats[0]['rank']
            lp = stats[0]['leaguePoints']
            wins = stats[0]['wins']
            losses = stats[0]['losses']
            win_rate = wins / (wins + losses) * 100
            win_rate = round(win_rate, 2)

            respond = tier + " " + rank + " " + str(lp) + " lp\nWins: " + str(
                wins) + " Losses: " + str(losses) + "\nWin rate: " + str(
                    win_rate) + "%"

            await ctx.send(respond)
        except IndexError:
            await ctx.send("Unranked")
    except ApiError as err:
        if err.response.status_code == 404:
            await ctx.send("Nincs ilyen idéző!")
        elif err.response.status_code == 401:
            await ctx.send("API kulcs error!")
        else:
            await ctx.send("Hiba!")


# Run the bot
bot.run(auth[1])


