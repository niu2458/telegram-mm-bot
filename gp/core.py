"""
Main bot functionnalities, core from gp module.
Author: Aryan Gholizadeh:aryghm@gmail.com
Project's github link: https://github.com/AryanGHM/telegram-gp-bot

"""
from telethon import events
from . import httpmethods, actions
import logging

"""
These functions will either forward the event to gp.filters or
gp.actions.

Functions are programmed asynchronously in order to be used 
with telethon.

Each function will take two arguments:
:param_telethon.events.Event event: This is the event that is first recieved
from telethon events.

:param_telethon.TelegramClient bot: The main telegram client to actually do stuff 
with it.

""" 

""" EVENT HANDLERS """

async def lockchat(event, bot):
    await actions.lockchat(event, bot)

async def unlockchat(event, bot):
    await actions.unlockchat(event, bot)

async def lockmedia(event, bot):
    await actions.lockmedia(event, bot)

async def unlockmedia(event, bot):
    await actions.unlockmedia(event, bot)

async def lockgif(event, bot):
    await actions.lockgif(event, bot)
async def unlockgif(event, bot):
    await actions.unlockgif(event, bot)
async def locksticker(event, bot):
    await actions.locksticker(event, bot)
async def unlocksticker(event, bot):
    await actions.unlocksticker(event, bot)

""" ~EVENT HANDLERS """

    
