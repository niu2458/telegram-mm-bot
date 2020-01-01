"""
Filters, can be enabled to detect an entity in a message (such as link) and 
delete the message also warn the user.
Author: Aryan Gholizadeh:aryghm@gmail.com
Project's github link: https://github.com/AryanGHM/telegram-gp-bot

"""
from . import utils, httpmethods, local_files
from telethon.tl import types

#filter the message if it has a link in it
async def filterlink(event, bot, group_prefs): 
    #Don't filter admins/creators
    if httpmethods.is_member_admin(await utils.get_channel_username(bot, event.to_id), event.from_id, local_files.get_bot_token()):
        return    
    
    if event.entities:
        for e in event.entities:
            if type(e) == types.MessageEntityUrl or type(e) == types.MessageEntityTextUrl:
                #message has link entity in it. Delete the message and warn the sender
                await utils.delete_message(bot, 
                                           event.id, 
                                           group_prefs.get_gp_name()
                                           )
                
                warning_db_path = group_prefs.get_warn_db_path()
                utils.increase_warn(warning_db_path, event.from_id, 1, group_prefs.get_max_warn())
                
                user_warnings = utils.get_warn(warning_db_path, event.from_id)
                if user_warnings >= group_prefs.get_max_warn():
                    #ban the user if exceeded maximum number of warnings
                    if await utils.ban_by_msg(event):
                        await event.reply("Banned user because of exceeding maximum number of warnings.")
                        return
                
                await event.reply("Don't send links! You've been warned for this action, You have {0}/{1} warning(s)."
                    .format(user_warnings, group_prefs.get_max_warn()))

#filter the message if it is forwarded
async def filterforward(event, bot, group_prefs): 
    #Don't filter admins/creators
    if httpmethods.is_member_admin(await utils.get_channel_username(bot, event.to_id), event.from_id, local_files.get_bot_token()):
        return    
    
    if event.forward:
        #message has a forward property which means it is forwarded
        await utils.delete_message(bot, 
                                   event.id, 
                                   group_prefs.get_gp_name()
                                   )
        
        warning_db_path = group_prefs.get_warn_db_path()
        utils.increase_warn(warning_db_path, event.from_id, 1, group_prefs.get_max_warn())
        
        user_warnings = utils.get_warn(warning_db_path, event.from_id)
        if user_warnings >= group_prefs.get_max_warn():
            #ban the user if exceeded maximum number of warnings
            if await utils.ban_by_msg(event):
                await event.reply("Banned user because of exceeding maximum number of warnings.")
                return
        
        await event.reply("Don't forward messages! You've been warned for this action, You have {0}/{1} warning(s)."
            .format(user_warnings, group_prefs.get_max_warn()))