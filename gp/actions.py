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

""" ~EVENT HANDLERS """