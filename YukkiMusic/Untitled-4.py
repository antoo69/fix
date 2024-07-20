#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#

from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types import Update
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream
from youtube_dl import Youtube

cookies= 'youtube_cookies.txt'

app = Client("my_bot")
pytgcalls = PyTgCalls(app)

@app.on_message(filters.command("play"))
async def play(client: Client, message: Message):
    url = message.text.split(" ", 1)[1]
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            'cookiesfile": youtube_cookies.txt,
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        audio_file = ydl.prepare_filename(info_dict).replace('.webm', '.mp3')
    
    chat_id = message.chat.id
    await pytgcalls.join_group_call(
        chat_id,
        InputStream(
            InputAudioStream(
                audio_file
            )
        )
    )
    await message.reply(f"Playing {info_dict['title']}")

@app.on_message(filters.command("stop"))
async def stop(client: Client, message: Message):
    chat_id = message.chat.id
    await pytgcalls.leave_group_call(chat_id)
    await message.reply("Stopped playing music!")

@pytgcalls.on_stream_end()
async def on_stream_end(client: PyTgCalls, update: Update):
    chat_id = update.chat_id
    await pytgcalls.leave_group_call(chat_id)

app.run()
