"""
Main bot setups, add and create threads for groups
Author: Aryan Gholizadeh:aryghm@gmail.com
Project's github link: https://github.com/AryanGHM/telegram-gp-bot

"""
from telethon import TelegramClient, events, utils, types
from telethon.tl import functions
import logging
import threading
from gp.core import GroupPolice

API_ID = 1121112
API_HASH =  "4e339ace3887950cdcda6a45d0d1fe93"
BOT_TOKEN = "1006932084:AAGhTF6wk6aXvb8wHDQ6pJm_OFlAntRzYeA"

DEBUG = True #debug flag

#the very main loop
with TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN) as bot:
    """
    For activating user first needs to start bot, then we send instructions:
    1.Add and promote bot in the supergroup
    2.Send "/activate <Channel id without 't.me/'>" back to us.
    
    Then we create a thread using GroupPolice object from gp.core. We will 
    take care of the rest from there.
    """
    #set logging debug messages if debug is enabled
    #set DEBUG to False if you want it disabled.
    if DEBUG:
        logging.basicConfig(level=logging.DEBUG)
    
    #Show welcome message if /start is sent
    @bot.on(events.NewMessage(pattern="/start"))
    async def guide(event):
        peer_type = type(await bot.get_input_entity(event.from_id)) #get peer type
        #Should not be called from a chat or channel
        if peer_type != types.InputUser:
            return        
        
        #Send a welcome message at first
        await event.reply("""
        Oh Hey! Welcome to the GroupPolice bot. I can assist
you with managing your group. No Ads, No nothing.
        
In order to activate me follow these steps:
    1.Add me to your group and promote me to admin.
        
    2.Send /activate <Your group id without t.me/> back to me.
    
    If you do both of these steps right you will get an 
    acknowledge message in the group.
        """)
    
    #Activate a group also verify that referring 
    #peer is a user.
    @bot.on(events.NewMessage("/activate"))
    async def activate_gp(event):
        sender_input = await utils.get_input_peer(event.from_id) #message sender's input entity
        
        peer_type = type(sender_input)
        #Should not be activated from a chat or channel
        if peer_type != types.InputUser:
            return
        
        #Should not be called by a bot either
        if (await bot(functions.users.GetFullUserRequest(sender_input))).is_bot:
            return
        
        
    
    #Run the bot's loop
    bot.run_until_disconnected()
    