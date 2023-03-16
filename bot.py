"""Simple telegram bot for VIBESLOADER"""

# import redis.asyncio as redis
# import json
import os
from os import getenv

from pathlib import Path

from asyncio import sleep

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

from main import local_decoupling, youtube_decoupling, prepare_dir

import logging


# Make data dir if it was not created before
prepare_dir()

# logging.basicConfig(filename='logs/vibesloader.log', encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


bot = Bot(token=getenv("TOKEN"))
dp = Dispatcher(bot)


# connection_redis = redis.Redis()


# TODO: add redis channel listener for signal from cron-parser
# TODO: make redis in-localhost only (check!)
# https://stackoverflow.com/questions/40114913/allow-redis-connections-from-only-localhost

# TODO: try this https://stackoverflow.com/a/61757914 for redis var en/decoding

# async def user_register(user):
#     print(f"New USER was registered: {user.full_name} (ID:{user.id})")

#     users = await connection_redis.get("allo_xiaomi_users")
#     if users:
#         users = json.loads(users)
#         new_users = set(users)
#         new_users.add(user.id)
#     else:
#         new_users = [user.id]

#     await connection_redis.mset({"allo_xiaomi_users": json.dumps(list(new_users))})

#     print(f"All users pack: {new_users}")


# TODO: unregister user and all user links for analyze? or just hold...
@dp.message_handler(commands="stop")
async def stop(message: types.Message):
    pass


@dp.message_handler(commands="start")
async def start(message: types.Message):

    # TODO: check if user is in DB/cache

    # message.from_id, message.from_user
    # await user_register(user=message.from_user)

    await message.answer("Just send me youtube link to decouple its audio vibes.")


# youtube links (for now only youtube can do)
# TODO: check for youtube links
# TODO: other online stuff sites
@dp.message_handler(Text(startswith="https://"))
async def link_usage(message: types.Message):
    await message.answer("Wait for result...")

    result, msg = youtube_decoupling(message.text)
    # if no errors - send mp3 file back to user
    if result:
        filemp3 = types.InputFile(msg)
        await message.answer_audio(filemp3)
        # delete files after success sending
        os.remove(msg)
        # TODO: delete file after success sending
    else:
        await message.answer(f"ErrorCode: {msg}")


# TODO 1/2: doc_usage + file_usage => to 1 universal function
# local document from msgs with video mime
@dp.message_handler(content_types=[types.ContentType.DOCUMENT])
async def doc_usage(message: types.Message):
    await message.answer("Wait for result...")

    if not message.document.mime_subtype[0] == "video":
        info = await message.document.get_file()
        # print(info)
        filepath = f"tmp/{message.document.file_name}"

        # TODO: if this message have "comment" - use it as filename.mp3 (after some mods | if it has mp3 in comment - use as it is)

        await message.document.download(destination_file=filepath)

    result, msg = local_decoupling(filepath)
    # if no errors - send mp3 file back to user
    if result:
        filemp3 = types.InputFile(msg)
        await message.answer_audio(filemp3)
        # delete files after success sending
        os.remove(filepath)
        os.remove(msg)
        # TODO: delete files after success sending
    else:
        await message.answer(f"Error: {msg}")


# TODO 2/2: doc_usage + file_usage => to 1 universal function
# local video files from msgs
@dp.message_handler(content_types=[types.ContentType.VIDEO, types.ContentType.VIDEO_NOTE])
async def file_usage(message: types.Message):
    await message.answer("Wait for result...")

    if not message.content_type == types.ContentType.VIDEO_NOTE:
        info = await message.video.get_file()
        # print(info)
        fileext = Path(info['file_path']).suffix
        filepath = f"tmp/{info['file_unique_id']}{fileext}"

        # TODO: if this message have "comment" - use it as filename.mp3 (after some mods | if it has mp3 in comment - use as it is)

        await message.video.download(destination_file=filepath)
    else:
        info = await message.video_note.get_file()
        # print(info)
        fileext = Path(info['file_path']).suffix
        filepath = f"tmp/{info['file_unique_id']}{fileext}"

        # TODO: if this message have "comment" - use it as filename.mp3 (after some mods | if it has mp3 in comment - use as it is)

        await message.video_note.download(destination_file=filepath)

    result, msg = local_decoupling(filepath)
    # if no errors - send mp3 file back to user
    if result:
        filemp3 = types.InputFile(msg)
        await message.answer_audio(filemp3)
        # delete files after success sending
        os.remove(filepath)
        os.remove(msg)
    else:
        await message.answer(f"Error: {msg}")


if __name__ == "__main__":
    executor.start_polling(dp)


# TODO: script arguments
# TODO: --no-verbose , logging
