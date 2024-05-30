import discord
import asyncio
import youtube_dl
from discord.ext import commands
from youtube_search import YoutubeSearch

baseurl = "https://op.gg/summoner/userName="

client = discord.Client()
que = {}
playlist = list()  # 재생목록 리스트
thumblink = list()
bot = commands.Bot(command_prefix="!")

async def Rplay(voice, i):
    try:
        if not voice.is_playing() and not voice.is_paused():
            ydl_opts = {'format': 'bestaudio'}
            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                              'options': '-vn'}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f'https://www.youtube.com{playlist[i][1]}', download=False)
                URL = info['formats'][0]['url']

            voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))

        while voice.is_playing() or voice.is_paused():
            await asyncio.sleep(0.1)
    except:
        return


def set_Embed(title='', description=''):
    # embed = discord.Embed(title="메인 제목", description="설명", color=0x62c1cc)
    return discord.Embed(title=title, description=description)

@bot.command(aliases=['play', 'p', 'ㅔ'])
async def Play(ctx, *, word):

    channel = ctx.author.voice.channel
    if bot.voice_clients == []:
        await channel.connect()
        # await ctx.send("connected to the voice channel, " + str(bot.voice_clients[0].channel))
    voice = bot.voice_clients[0]
    results = YoutubeSearch(word, max_results=1).to_dict()
    title =  f"{results[0]['title']}"
    urllink = ('https://www.youtube.com' + results[0]['url_suffix'])
    thumbnails=f"{results[0]['thumbnails'][0]}"
    duration=f"{results[0]['duration']}"

    embed = discord.Embed(title='노래 추가', description=f"{title}")
    embed.set_thumbnail(url=f"{thumbnails}")
    embed.add_field(name="재생 시간", value=f"{duration}", inline=True)
    embed.add_field(name="노래 링크", value=f"{urllink}", inline=True)
    embed.set_footer(text="{}".format(ctx.author), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


    global playlist
    playlist.append([results[0]['title'], results[0]['url_suffix']])  # 플레이리스트에 노래 추가


    if not voice.is_playing() and not voice.is_paused():
        global i
        i = 0
        while True:
            await Rplay(voice, i)
            if i < len(playlist) - 1:
                i = i + 1
                continue
            playlist = [[]]
            break
    # await voice.disconnect()



@bot.command(aliases=['q', 'ㅂ'])
async def Que(ctx):
    try:
        queText = ''
        for title in range(len(playlist)):
            try:
                queText = f'{queText}\n' + f'{title + 1}. {playlist[title][0]}'
            except:
                del playlist[title]
        await ctx.send(embed=set_Embed(title='플레이리스트', description=f"{queText}"))
    except:
        pass


@bot.command(aliases=['remove'])
async def Remove(ctx, arg):
    try:
        global playlist
        remove_song = playlist[int(arg) - 1][0]
        del (playlist[int(arg) - 1])
        global i
        i = i - 1
        if (i + 1) == int(arg) - 1:
            bot.voice_clients[0].stop()
        await ctx.send(embed=set_Embed(title='노래 삭제', description=f"{remove_song}"))
    except:
        await ctx.send('노래 제거중 오류 발생!')


@bot.event
async def on_ready():
    print('Loggend in Bot: ', bot.user.name)
    print('Bot id: ', bot.user.id)
    print('connection was succesful!')
    print('=' * 30)


@bot.command(aliases=['안녕', 'ㅎㅇ'])
async def Hello(ctx):
    await ctx.send("{}, 안녕!".format(ctx.author.mention))


@bot.command()
async def 이(ctx):
    await ctx.send("바보")


@bot.command()
async def 박(ctx):
    await ctx.send("돼지") \
    @ bot.command()


async def 한(ctx):
    await ctx.send("빅토르")


@bot.command()
async def echo(ctx, *, msg):
    await ctx.send(msg)


@bot.command(aliases=['명령어', '도움'])
async def embed(ctx):
    embed = discord.Embed(title="노래봇", decsription="디스크립션", color=0xFFFFFF)
    embed.set_thumbnail(url="https://upload3.inven.co.kr/upload/2021/08/22/bbs/i13912768838.png")
    embed.add_field(name="안녕하세요", value="안녕하세요, 반갑습니다.", inline=False)
    embed.add_field(name="!play, !ㅔ, !p", value="노래추가 (아직 재생목록은 못함 한번에 한곡)", inline=False)
    embed.add_field(name="!skip, !s", value="노래 스킵", inline=False)
    embed.add_field(name="!정지, !stop", value="노래 일시 정지", inline=False)
    embed.add_field(name="!resume, !r", value="노래 일시 정지 해제", inline=False)
    embed.add_field(name="!que, !q, !ㅂ", value="현재 플레이리스트", inline=False)
    embed.add_field(name="!remove", value="플레이리스트에서 노래 제거", inline=False)
    embed.add_field(name="제작자", value="강은석", inline=False)
    embed.set_footer(text="Bot Made by kes#1999", icon_url="https://i.ibb.co/1rPz2gs/ghost.png")
    await ctx.send(embed=embed)


@bot.command(name='관리자')
async def mangerCheck(ctx):
    if ctx.guild:
        if ctx.message.author.guild_permissions.administrator:
            await ctx.send('이 서버의 관리자입니다.')
        else:
            await ctx.send('이 서버의 관리자가 아닙니다.')
    else:
        await ctx.send('DM으론 불가능합니다.')


@bot.command(name='공지작성')
async def Announcement(ctx, *, notice):
    i = ctx.message.author.guild_permissions.administrator
    channel = ctx.guild.get_channel(921360333451436033)  # 메시지를 보낼 채널 설정
    # Discord 에서 개발자 모드를 켜서 채널의 ID를 가져와 넣는다.

    if i is True:
        embed = discord.Embed(title="**Red_Cat 공지사항**",
                              description="공지사항은 항상 잘 숙지 해주시기 바랍니다.\n――――――――――――――――――――――――――――\n\n{}\n\n――――――――――――――――――――――――――――".format(
                                  notice),
                              color=0x2EFEF7)
        embed.set_footer(text="Bot made by. kes#1999 | 담당 관리자: {}".format(ctx.author),
                         icon_url="https://imgur.com/1fTB9uk.png")
        await channel.send("@everyone", embed=embed)
        await ctx.send(
            "```**[ BOT 자동 알림 ]** | 정상적으로 공지가 채널에 작성이 완료되었습니다 : )\n\n[ 기본 작성 설정 채널 ] : {}\n[ 공지 발신자 ] : {}\n\n[ 내용 ]\n{}```".format(
                channel, ctx.author, notice))

    if i is False:
        await ctx.send("{}, 당신은 관리자가 아닙니다".format(ctx.author.mention))


@bot.command()
async def leave(ctx):
    await bot.voice_clients[0].disconnect()


@bot.command(aliases=['정지', 'stop'])
async def pause(ctx):
    if not bot.voice_clients[0].is_paused():
        bot.voice_clients[0].pause()
        await ctx.send("일시정지")
    else:
        await ctx.send("already paused")


@bot.command(aliases=['재시작', 'r'])
async def resume(ctx):
    if bot.voice_clients[0].is_paused():
        bot.voice_clients[0].resume()
        await ctx.send("재시작")
    else:
        await ctx.send("already playing")


@bot.command(aliases=['s'])
async def skip(ctx):
    if bot.voice_clients[0].is_playing():
        bot.voice_clients[0].stop()
        await ctx.send("스킵")
    else:
        await ctx.send("not playing")


bot.run('OTIyNzc0NzUyODgyNDc1MDQ5.YcGW9Q.KYc5VLhE23TzHNS2a7SU8BI10sw')
client.run('OTIyNzc0NzUyODgyNDc1MDQ5.YcGW9Q.KYc5VLhE23TzHNS2a7SU8BI10sw')
# 참고사이트
# https://discordpy.readthedocs.io/en/stable/api.html
# https://howbeautifulworld.tistory.com/52?category=1033433
# https://lektion-von-erfolglosigkeit.tistory.com/96
# https://github.com/alexmercerind/youtube-search-python
# https://stackoverflow.com/questions/59779193/python-youtube-search-how-to-get-link
