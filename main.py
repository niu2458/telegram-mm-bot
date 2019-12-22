"""
Main bot setups, add and create threads for groups
Author: Aryan Gholizadeh:aryghm@gmail.com
Project's github link: https://github.com/AryanGHM/telegram-gp-bot

"""
from telethon import TelegramClient, events, utils, types
from telethon.tl import functions
import logging
from gp import core, httpmethods

API_ID = 1121112
API_HASH =  "4e339ace3887950cdcda6a45d0d1fe93"
BOT_TOKEN = "1006932084:AAGhTF6wk6aXvb8wHDQ6pJm_OFlAntRzYeA"

"""
We will only manage these chats. The events will only trigger
when messages are recieved from these chats. This is our white
list indeed.

"""
CHATS = []

DEBUG = True #debug flag

#the very main loop
with TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN) as bot:
    """
    For activating user first needs to start bot, then we send instructions:
    1.Add and promote bot in the supergroup
    2.Send "/activate <Channel id without 't.me/'>" back to us.
    
    In order to manage groups we forward our events to "gp.core" module. Events 
    are only triggered if a message is coming from a chat that is in CHATS list.
    
    As we limit our events to only trigger by whitelisted 
    chats  if we add a group's entity to our white list we 
    indeed activated it.
    """
    
    #set logging debug messages if debug is enabled
    #set DEBUG to False if you want it disabled.
    if DEBUG:
        logging.basicConfig(level=logging.DEBUG)
            
    #This function verifies that a channel
    #is in CHATS whitelist or not
    #:param telethon.types.PeerChannel channel: the channel to verify
    async def verify_whitelist(channel):
        # get username of channel
        channel_name = (await bot(functions.channels.GetChannelsRequest([channel]))).chats[0].username
        if channel_name in CHATS:
            return True
        else:
            return False
        
    
    
    """ EVENTS """
    
    @bot.on(events.NewMessage(pattern="/lockchat"))
    async def lchat(event):
        #Verify the input peer with whitelist
        if not (await verify_whitelist(event.to_id)):
            return
            
        await core.lockchat(event, bot)
    
    """ ~EVENTS """
    
    #Activate a group also verify that referring peer is a user.
    @bot.on(events.NewMessage(pattern="/activate"))
    async def activate_gp(event):
        global CHATS
        #Should not be called in a group or supergroup
        if type(event.to_id) != types.PeerUser:
            return  
        
        #Should not be called from a bot either
        if (await bot(functions.users.GetFullUserRequest(event.from_id))).user.bot:
            return        
        
        #Finnaly activate the group
        #Try to get group's username from the mesasge
        try:
            group_name = event.raw_text.split()[1]
        except IndexError: 
            await event.reply("If you want to activate a group send:\n__/activate <Your group username without t.me/>__")
            return
        
        CHATS.append(group_name)
        
        #Test for admin priviledges and send acknowledgements.
        self_status = httpmethods.get_chat_member_status(group_name, 
                                                      BOT_TOKEN.split()[0],
                                                      BOT_TOKEN)   #first segment of bot api token seperated by ':' is the bot user id     
        if "administrator" in self_status:
            await bot.send_message(group_name, "Group Police is successfully activated in your group.")
            await event.reply("Done! I will send an acknowledge message in the group too.")
        else:
            await event.reply("Woops! Looks like I'm either not joined/promoted in the group!")        
    
    
    #Show welcome message if /start is sent
    @bot.on(events.NewMessage(pattern="/start"))
    async def guide(event):
        #Should not be called in a group or supergroup
        if type(event.to_id) != types.PeerUser:
            return  
        
        #Should not be called from a bot either
        if (await bot(functions.users.GetFullUserRequest(event.from_id))).user.bot:
            return
        
        #Send a welcome message at first
        await event.reply("""
        Oh Hey! Welcome to the GroupPolice bot. I can assist
you with managing your group. No Ads, No nothing.
        
In order to activate me follow these steps:
    1.Add me to your group and promote me to admin.
        
    2.Send __/activate <Your group id without t.me/>__ back to me.
    
    If you do both of these steps right you will get an 
    acknowledge message in the group.
        """)
    
    
    
    #Run the bot's loop
    bot.run_until_disconnected()
    