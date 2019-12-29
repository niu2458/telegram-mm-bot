"""
Utility functions used across all gp bot.
Author: Aryan Gholizadeh:aryghm@gmail.com
Project's github link: https://github.com/AryanGHM/telegram-gp-bot

"""
from telethon import TelegramClient, functions

"""
Get username of a channel from it's peer (eg. Message.to_id)

:param)telethon.TelegramClient bot: A live telegram api client to use.

:param_telethon.types.PeerChannel channel: The channel to get username of

"""
async def get_channel_username(bot, channel):
    return (await bot(functions.channels.GetChannelsRequest([channel]))).chats[0].username