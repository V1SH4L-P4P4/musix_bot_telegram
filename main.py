#commits: imported hqaudio
#         added to join/skip -> hqaudio in pipe

from email.mime import audio
from pyrogram import filters
from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls import idle
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types import HighQualityAudio
import yt_dl

#chat_id = -1001522096029 #-735193965
link = [] #"D:\games\My Money Dont Jiggle Jiggle.mp3"

txt = """
/j(oin) - __Bot joins active voice chat__
/p(lay) - __Do /play [link] to queue__
/q(ueue) - __Return Queue list__
/s(kip) - __Skip current playing song__
/pas(res) - __Pause/Resume current playing music__**(Unavailable)**
[/dc](https://influencersgonewild.com/) - **Disconnect T-T**
"""

'''api_id = 17775109
api_hash = '304c269678f38763e8c344e8ce63f0d7'
bot_token = '5565363119:AAHQtL6UAZaHVjecmmRrses8UAH-hPx2Ha0'
'''
session = 'BQEPOgUALBIyEp3MAdXLKHuOP6y7Gt6Pgf_wCccBf_43mJi3_l1xbkg6zu0z-_bN887ATJXbhsIvVfeAmnQRBTx3Y3vav9u0UNZN-31EVR4ctfR2vpxQ6bwb74LcDpdwtsuzc_aOGQPG5pCZ0qUjENMfmDyThux-JiNHyuXgdYWeNK8toIHUlhRK7XedeD6ayqpJX--bpYawoMsDTXwhD0RFNu_jnQjnV66H95hzjnuDc9b8W-Y0fGYBOn5F2P4TcTy1ZCahdqSSPGkAJ-4CtIPioIPmx8SFGGXz_Cd4lVrFmcWdwkzNFrQGfJKN26c5PgvQfyC46hzgoO8jhaafZwnfuezthwAAAAFNjyTfAA'

ffmpegoptions = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'}

#<----Client Called---->
app = Client("music_bot", session_string=session)
app_call = PyTgCalls(app)

#<----Handlers---->
@app.on_message(filters.command(['start','start@Musix_bot2']))
async def start(client, message):
    await app.send_message(message.chat.id, f"Hey {message.chat.first_name},\nDo /help for bot commands...")

@app.on_message(filters.command(["help", "help@Musix_bot2"]))
async def help(client, message):
    await app.send_message(message.chat.id, txt, disable_web_page_preview=True)

@app.on_message(filters.command(["clearlist"]))
async def clearlist(client, message):
    if not(bool(link)):
        await app.send_message(message.chat.id, "<pre>List is already clear</pre>")
    else:
        link.clear()
        await app.send_message(message.chat.id, "<pre>List is now empty</pre>")

@app.on_message(filters.command(["p","play","p@Musix_bot2", "play@Musix_bot2"]))
async def play(client, message):
    msg = message.text
    try:
        link_req = msg.split("/p")[1].strip()
        if link_req in link:
            await message.reply("<pre>Already in queue list</pre>")
        elif link_req == '':
            await message.reply("**Invalid**\n__Do /p [link]__")
        elif "https://" in link_req:
            link.append(link_req)  #play krne ke baad pop krwana h
            await app.send_message(message.chat.id, "<pre>Added to queue list</pre>")
        else:
            await app.send_message(message.chat.id, "Youtube ka link daal bhai share mai se..")

    except:
        await message.reply("Invalid link")

@app.on_message(filters.command(['q','queue','q@Musix_bot2','queue@Musix_bot2']))
async def queue(client, message):
    if len(link) > 0:
        for i in link:
            await app.send_message(message.chat.id, i, disable_web_page_preview=True)
    else:
        await app.send_message(message.chat.id, "<pre>Queue list is empty</pre>")


@app.on_message(filters.command(["pas","res","pas@Musix_bot2", "res@Musix_bot2"]))
async def pause_or_resume(client ,message):
    print(link[0])

@app.on_message(filters.command(['dc', 'disconnect','dc@Musix_bot2', 'disconnect@Musix_bot2']))
async def disconnect(client, message):
    await app_call.leave_group_call(message.chat.id)


@app.on_message(filters.command(["s","skip","s@Musix_bot2", "skip@Musix_bot2"]))
async def skip(client, message):
    src_url = yt_dl.src_find(link[0])
    await app_call.change_stream(message.chat.id, AudioPiped(src_url, audio_parameters=HighQualityAudio()))
    del link[0]

@app.on_message(filters.command(["j", "join", "j@Musix_bot2", "join@Musix_bot2"]))
async def join(client, message):       
    try:
        src_url = yt_dl.src_find(link[0])        
        await app_call.join_group_call(message.chat.id, AudioPiped(src_url, audio_parameters=HighQualityAudio()), stream_type=StreamType().pulse_stream)
        del link[0]
        #await app.send_message(message.chat.id, "__Joining...__")
    except:
        await app.send_message(message.chat.id, "No active Group calls or,\nMaybe __queue list__ is empty.\nDo /q to get __queue list__")

#Chat join/Play music
'''app_call.start()
app_call.join_group_call(chat_id, AudioPiped(link))
idle()'''

app_call.start()
idle()
