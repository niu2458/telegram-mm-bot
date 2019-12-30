"""
Bot actions, like locking chat or gif or media sharing etc.
Author: Aryan Gholizadeh:aryghm@gmail.com
Project's github link: https://github.com/AryanGHM/telegram-gp-bot

"""
from telethon import functions, types
from .httpmethods import is_member_admin
from . import utils, local_files

BOT_TOKEN = local_files.get_bot_token()

""" EVENT HANDLERS """

async def ban(event, bot):
    #make sure that calling user is an admin or creator
    if not is_member_admin(await utils.get_channel_username(bot, event.to_id), event.from_id, BOT_TOKEN):
        await event.reply("You Cannot Do That!!")
        return
    
    #ban the sender of replied message
    try:
        target_id = (await event.get_reply_message()).from_id
    except AttributeError:
        #this is raised when the object returned by "get_reply_message" 
        #is None.this means user didn't reply anyone to warn
        await event.reply("Please reply a message from the user you want banned.")
        return        
    
    await bot.edit_permissions(await bot.get_input_entity(event.to_id),
                                                   await bot.get_input_entity(target_id), 
                                                   view_messages=False,
                                                   )     
    
    await event.reply("Banned user")

async def unban(event, bot):
    #make sure that calling user is an admin or creator
    if not is_member_admin(await utils.get_channel_username(bot, event.to_id), event.from_id, BOT_TOKEN):
        await event.reply("You Cannot Do That!!")
        return
    
    #ban the sender of replied message
    try:
        target_id = (await event.get_reply_message()).from_id
    except AttributeError:
        #this is raised when the object returned by "get_reply_message" 
        #is None.this means user didn't reply anyone to warn
        await event.reply("Please reply a message from the user you want unbanned.")
        return        
    
    await bot.edit_permissions(await bot.get_input_entity(event.to_id),
                                                   await bot.get_input_entity(target_id), 
                                                   view_messages=True,
                                                   )     
    
    await event.reply("Unbanned user, you may add him now.")    


"""
Warning system, 
We use an sqlite database to hold warnings for each user.
Each group has it's own database and it's path is stored under the group's Group Preferences
file (.grprf).There are other values such as max warning count also stored under the ".grprf"
file.

Group Preferences are handled by "local_files" module although warning system values are fetched
and passed by main module to us.

Warning databases are handled by gp.utils module.

"""
async def warn(event, bot, group_prefs):
    #make sure that calling user is an admin or creator
    if not is_member_admin(await utils.get_channel_username(bot, event.to_id), event.from_id, BOT_TOKEN):
        await event.reply("You Cannot Do That!!")
        return
    
    #warn the sender of the replied message
    try:
        target_id = (await event.get_reply_message()).from_id
    except AttributeError:
        #this is raised when the object returned by "get_reply_message" 
        #is None.this means user didn't reply anyone to warn
        await event.reply("Please reply a message from the user you want warned.")
        return    
    
    #if the sender is an admin or creator abort
    if is_member_admin(await utils.get_channel_username(bot, event.to_id), target_id, BOT_TOKEN):
        return
    
    #get path of warning database of the group
    warn_db = group_prefs.get_warn_db_path()
    
    utils.increase_warn(warn_db, target_id, 1, group_prefs.get_max_warn())
    
    #if the warning count of the user has exceeded ban the user
    user_warning_count = utils.get_warn(warn_db, target_id)
    if user_warning_count >= group_prefs.get_max_warn():
        await ban(event, bot)
        await (await event.get_reply_message()).reply("Banning you because of getting maximum warnings")
    else:
        await (await event.get_reply_message()).reply(
            "You got a warning, You have {0}/{1} warnings.\nIf you get {1} you will be banned".format(user_warning_count, group_prefs.get_max_warn()))
    
async def dewarn(event, bot, group_prefs):
    #make sure that calling user is an admin or creator
    if not is_member_admin(await utils.get_channel_username(bot, event.to_id), event.from_id, BOT_TOKEN):
        await event.reply("You Cannot Do That!!")
        return
    
    #warn the sender of the replied message
    try:
        target_id = (await event.get_reply_message()).from_id
    except AttributeError:
        #this is raised when the object returned by "get_reply_message" 
        #is None.this means user didn't reply anyone to warn
        await event.reply("Please reply a message from the user you want dewarned.")
        return    
    
    #if the sender is an admin or creator abort
    if is_member_admin(await utils.get_channel_username(bot, event.to_id), target_id, BOT_TOKEN):
        return
    
    #get path of warning database of the group
    warn_db = group_prefs.get_warn_db_path()
    
    utils.decrease_warn(warn_db, target_id, 1, group_prefs.get_max_warn())
    
    #if the warning count of the user has exceeded ban the user
    user_warning_count = utils.get_warn(warn_db, target_id)
    await (await event.get_reply_message()).reply(
        "You got a warning, You have {0}/{1} warnings.\nIf you get {1} you will be banned".format(user_warning_count, group_prefs.get_max_warn()))




""" RESTRICTORS """
async def lockchat(event, bot):
    #make sure that calling user is an admin or creator
    if not is_member_admin(await utils.get_channel_username(bot, event.to_id), event.from_id, BOT_TOKEN):
        await event.reply("You Cannot Do That!!")
        return
    
    await bot.edit_permissions(await bot.get_input_entity(event.to_id),
                                                   None, #change the default permission
                                                   send_messages=False,
                                                   ) 
    
    
    await event.reply("Locked Chat")
        
async def unlockchat(event, bot):
    #make sure that calling user is an admin or creator
    if not is_member_admin(await utils.get_channel_username(bot, event.to_id), event.from_id, BOT_TOKEN):
        await event.reply("You Cannot Do That!!")
        return
    
    await bot.edit_permissions(await bot.get_input_entity(event.to_id),
                                                   None, #change the default permission
                                                   send_messages=True,
                                                   )
    
    await event.reply("Unlocked Chat")    

async def lockmedia(event, bot):
    #make sure that calling user is an admin or creator
    if not is_member_admin(await utils.get_channel_username(bot, event.to_id), event.from_id, BOT_TOKEN):
        await event.reply("You Cannot Do That!!")
        return
    
    await bot.edit_permissions(await bot.get_input_entity(event.to_id),
                                                   None, #change the default permission
                                                   send_media=False,
                                                   )
    
    await event.reply("Locked Media Sharing")  

async def unlockmedia(event, bot):
    #make sure that calling user is an admin or creator
    if not is_member_admin(await utils.get_channel_username(bot, event.to_id), event.from_id, BOT_TOKEN):
        await event.reply("You Cannot Do That!!")
        return
    
    await bot.edit_permissions(await bot.get_input_entity(event.to_id),
                                                   None, #change the default permission
                                                   send_media=True,
                                                   )
    
    await event.reply("Unlocked Media Sharing")  

async def lockgif(event, bot):
    #make sure that calling user is an admin or creator
    if not is_member_admin(await utils.get_channel_username(bot, event.to_id), event.from_id, BOT_TOKEN):
        await event.reply("You Cannot Do That!!")
        return
    
    await bot.edit_permissions(await bot.get_input_entity(event.to_id),
                                                   None, #change the default permission
                                                   send_gifs=False,
                                                   )
    
    await event.reply("Locked Gif Sharing") 

async def unlockgif(event, bot):
    #make sure that calling user is an admin or creator
    if not is_member_admin(await utils.get_channel_username(bot, event.to_id), event.from_id, BOT_TOKEN):
        await event.reply("You Cannot Do That!!")
        return
    
    await bot.edit_permissions(await bot.get_input_entity(event.to_id),
                                                   None, #change the default permission
                                                   send_gifs=True,
                                                   )
    
    await event.reply("Unlocked Gif Sharing")  

async def locksticker(event, bot):
    #make sure that calling user is an admin or creator
    if not is_member_admin(await utils.get_channel_username(bot, event.to_id), event.from_id, BOT_TOKEN):
        await event.reply("You Cannot Do That!!")
        return
    
    await bot.edit_permissions(await bot.get_input_entity(event.to_id),
                                                   None, #change the default permission
                                                   send_stickers=False,
                                                   )
    
    await event.reply("Locked Sticker Sharing")  

async def unlocksticker(event, bot):
    #make sure that calling user is an admin or creator
    if not is_member_admin(await utils.get_channel_username(bot, event.to_id), event.from_id, BOT_TOKEN):
        await event.reply("You Cannot Do That!!")
        return
    
    await bot.edit_permissions(await bot.get_input_entity(event.to_id),
                                                   None, #change the default permission
                                                   send_stickers=True,
                                                   )
    
    await event.reply("Unlocked Sticker Sharing")    

""" ~RESTRICTORS """

""" ~EVENT HANDLERS """