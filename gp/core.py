"""
Main bot functionnalities, core from gp module.
Author: Aryan Gholizadeh:aryghm@gmail.com
Project's github link: https://github.com/AryanGHM/telegram-gp-bot

"""
from telethon import events
from . import httpmethods, actions, filters, utils, local_files
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

#A help message to help the admins with commands
HELP_MESSAGE = \
"""
Group Police Bot help manual,

Commands:
/help: Show this message 

/locklnk: Delete every message that contains links and warn the sender.
/unlocklnk: Undo above

/lockfwd: Delete every forwarded message and warn the sender.
/unlockfwd: Undo above

/ban: Ban the sender of the replied message, use /unban to unban the user so they can join by group's link.
/unban: Unban a user, he will be able to join the group via link or be added by a normal member.

/lockchat: Lock the chat for normal users (not admins).
/unlockchat: Undo above

/lockmedia: Lock media sharing (pics and videos) for normal users.
/unlockmedia: Undo above

/lockgif: Lock gif sharing for normal users.
/unlockgif: Undo above

/locksticker: Lock sticker sharing for normal users.
/unlocksticker: Undo above.

/warn: Warn the sender of the replied message. If the warning count of a user reaches maximum warnings he/she will be banned.
/dewarn: Decrease 1 warn from the warnings of the replied message sender.
/maxwarn __n__: Set maximum warning count to __n__


Bot by Aryan Gholizadeh(email: aryghm@gmail.com), Source code at:
https://github.com/AryanGHM/telegram-gp-bot
"""

BOT_TOKEN = local_files.get_bot_token()

""" EVENT HANDLERS """

""" FILTERS """
async def locklink(event, bot, group_prefs):
    #make sure that calling user is an admin or creator
    if not httpmethods.is_member_admin(await utils.get_channel_username(bot, event.to_id), event.from_id, BOT_TOKEN):
        await event.reply("You Cannot Do That!!")
        return    
    
    #enable the link locking
    group_prefs.set_filter(group_prefs.locklink, True)
    
    await event.reply("Link sharing is locked, every user that send link would be warned")
async def lockforward(event,bot, group_prefs):
    #make sure that calling user is an admin or creator
    if not httpmethods.is_member_admin(await utils.get_channel_username(bot, event.to_id), event.from_id, BOT_TOKEN):
        await event.reply("You Cannot Do That!!")
        return    
    
    #enable the forward locking
    group_prefs.set_filter(group_prefs.lockfwd, True)
    
    await event.reply("Forwarded mesasges are now locked, every user that forward a mesasge to this group will be warned")
async def unlocklink(event, bot, group_prefs):
    #make sure that calling user is an admin or creator
    if not httpmethods.is_member_admin(await utils.get_channel_username(bot, event.to_id), event.from_id, BOT_TOKEN):
        await event.reply("You Cannot Do That!!")
        return    
    
    #disable the link locking
    group_prefs.set_filter(group_prefs.locklink, False)
    
    await event.reply("Unlocked link sharing, users may now send links.")
async def unlockforward(event, bot, group_prefs):
    #make sure that calling user is an admin or creator
    if not httpmethods.is_member_admin(await utils.get_channel_username(bot, event.to_id), event.from_id, BOT_TOKEN):
        await event.reply("You Cannot Do That!!")
        return    
    
    #disable forward locking
    group_prefs.set_filter(group_prefs.lockforward, False)
    
    await event.reply("Unlocked forwarding messages, users may now forward messages.")
"""
Validate function checks for invalid entities in messages if there
is an invalid entity in the message it passes the entity to a filter
function to take care of the rest. See gp.filters for more info.

"""
async def validate(event, bot, group_prefs):
    #only forward if needed
    if group_prefs.get_filter(group_prefs.locklink):
        await filters.filterlink(event, bot, group_prefs)
    
    if group_prefs.get_filter(group_prefs.lockfwd):
        await filters.filterforward(event, bot, group_prefs)
        
""" RESTRICTORS """
async def setmaxwarn(event, bot, group_prefs, max_warn):
    if group_prefs.set_max_warn(max_warn):
        #Done 
        await event.reply("Maximum number of warnings has been set to {}".format(str(max_warn)))
    else:
        #Couldn't do
        await event.reply("Couldn't set maximum number of warnings, probably a wrong value?")
        
async def ban(event, bot):
    await actions.ban(event, bot)
async def unban(event, bot):
    await actions.unban(event, bot)
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
""" ~RESTRICTORS """

""" WARNING FUCNTIONS """
async def warn(event, bot, group_prefs):
    await actions.warn(event, bot, group_prefs)

async def dewarn(event, bot, group_prefs):
    await actions.dewarn(event, bot, group_prefs)

""" ~WARNING FUNCTIONS """

""" OTHERS """ 
async def showhelp(event, bot):
    #show a help message for group admin to use the bot
    await event.reply(HELP_MESSAGE)

""" ~EVENT HANDLERS """

    
