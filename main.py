#commits: audio src not found exceptions
# added search command 
# skip - join called/ added leavegrp
# join - leave if src not found
#changes in error handling for src file

import random
from pyrogram import filters
from pyrogram import Client
from pyrogram.types import Update

from pytgcalls import PyTgCalls
from pytgcalls import idle
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types import HighQualityAudio
from pytgcalls import exceptions as ex
from pytgcalls.types import StreamAudioEnded

import yt_dl
import yt_search
import sp_search
from time import sleep

#chat_id = -1001522096029 #-735193965
link = [] #"D:\games\My Money Dont Jiggle Jiggle.mp3"
approvallist = [1289504212]

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
    if bool(link):
        link.clear()
        await app.send_message(message.chat.id, "<pre>List is now empty</pre>")
    else:
        await app.send_message(message.chat.id, "<pre>List is already clear</pre>")

@app.on_message(filters.command(['pop']))
async def pop(client, message):
    msg = message.text
    index_no = msg.split("/pop")[1].strip() #pass not integer/out of index no
    try:
        #conversion
        converted = int(index_no)
    except ValueError:
        await app.send_message(message.chat.id, "__Argument not an integer.__")
    try: 
        del link[converted]
        await app.send_message(message.chat.id, "<pre>Removed from que list.</pre>")
    except IndexError:
        await app.send_message(message.chat.id, f"**Out of list index**\nOnly have {len(link)} items in queue")

@app_call.on_stream_end()
async def autostream(client:PyTgCalls, update:Update):
    if isinstance(update, StreamAudioEnded):
        try:
            await app_call.change_stream(update.chat_id, AudioPiped(yt_dl.src_find(link[0]), audio_parameters=HighQualityAudio()))
            del link[0]
        except:
            await app.send_message(update.chat_id, "Auto play inactive for now.")
            await app_call.leave_group_call(update.chat_id)

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

@app.on_message(filters.command(['artist']))
async def search(client, message):
    msg = message.text
    try:
        link_req = msg.split('/artist')[1].strip()
        music_list = sp_search.recommend(link_req)
        for i in range(0,5):
            select_music = random.choice(music_list)
            query_for_ytsearch = select_music + " " + link_req
            yt_search_music = yt_search.lookup(query_for_ytsearch)
            link.append(yt_search_music)
        await app.send_message(message.chat.id, "<pre>Added a 5 random songs from this artist to list</pre>")
        music_list.clear()
    except:
        await app.send_message(message.chat.id, "Nhi milra yrr..")

@app.on_message(filters.command(['search']))
async def search(client, message):
    msg = message.text
    link_req = msg.split('/search')[1].strip()
    url = yt_search.lookup(link_req)
    if url in link:
        await app.send_message(message.chat.id, "Already in queue")
    else:
        link.append(url)
        await app.send_message(message.chat.id, f"Query passed,\n{url}\n__Here is the url__")


@app.on_message(filters.command(['q','queue','q@Musix_bot2','queue@Musix_bot2']))
async def queue(client, message):
    if len(link) > 0:
        title = []
        for i in link:
            title.append(yt_search.search_title(i))
        temp_text = "\n".join(title)
        await app.send_message(message.chat.id, temp_text, disable_web_page_preview=True)
        title.clear()
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
    if message.from_user.id in approvallist:
        try:
            await app_call.leave_group_call(message.chat.id)
            await join(client, message)
        except ex.NoActiveGroupCall:
            await app.send_message(message.chat.id, "Not in a group call.")
    else:
        await app.send_message(message.chat.id, "You are not allowed to use this method.")

@app.on_message(filters.command(['approve']))
async def approve(client, message):
    if message.from_user.id == 1289504212:
        if message.reply_to_message.from_user.id in approvallist:
            await app.send_message(message.chat.id, "__User already allowed to use /s method.__")
        else:
            approvallist.append(message.reply_to_message.from_user.id)
            await app.send_message(message.chat.id, f"<pre>{message.reply_to_message.from_user.first_name} is now allowed to use skip method.</pre>")
    else:
        await app.send_message(message.chat.id, "Acha")

@app.on_message(filters.command(['disapprove']))
async def disapprove(client, message):
    if message.from_user.id == 1289504212:
        approvallist.remove(message.reply_to_message.from_user.id)
        await app.send_message(message.chat.id, "User removed from approval list now can't user /s method.")

@app.on_message(filters.command(["j", "join", "j@Musix_bot2", "join@Musix_bot2"]))
async def join(client, message):          
    try:
        src_url = yt_dl.src_find(link[0])        
        try:
            await app_call.join_group_call(message.chat.id, AudioPiped(src_url, audio_parameters=HighQualityAudio()), stream_type=StreamType().pulse_stream)
            del link[0]
        except ex.NoActiveGroupCall:
            await app.send_message(message.chat.id, "No active Group calls or,\nMaybe __queue list__ is empty.\nDo /q to get __queue list__")
        except ex.AlreadyJoinedError:
            await app.send_message(message.chat.id, "<pre>Already in a group call.</pre>")
            #await app.send_message(message.chat.id, "__Joining...__")
    except ex.NoAudioSourceFound:
        await app.send_message(message.chat.id, "No audio src found,\nDo /pop [index] to remove that from list.")
        await app_call.leave_group_call(message.chat.id)
    except IndexError:
        await app.send_message(message.chat.id, "__List is empty.__")

#Chat join/Play music
'''app_call.start()
app_call.join_group_call(chat_id, AudioPiped(link))
idle()'''

app_call.start()
idle()