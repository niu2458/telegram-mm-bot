"""
Main bot setups, add and create threads for groups
Author: Aryan Gholizadeh:aryghm@gmail.com
Project's github link: https://github.com/AryanGHM/telegram-gp-bot

"""
from telethon import TelegramClient, events, utils, types
from telethon.tl import functions
import logging
from gp import core, httpmethods, local_files
from gp import utils as gp_utils

API_ID = local_files.get_api_id()
API_HASH =  local_files.get_api_hash()
BOT_TOKEN = local_files.get_bot_token()

"""
We will only manage these chats. The events will only trigger
when messages are recieved from these chats. This is our white
list indeed.

Each of these chats have a "Group Preference" files, which contains 
preferences of these groups. These files are unique and they are 
persistence, that means they are kept even if the bot is restarted.

"""
CHATS = []

"""
This dictionary contains "GroupPrefs" class for each chat that is 
registered, this can be later used to fetch the GroupPrefs class
of each chat.

"""
PREFERENCES = {} 

DEBUG = True #debug flag

#a message to show in the group that has been activated
ACTIVATION_ACKNOWLEDGE_MESSAGE = \
    "Group Police bot by Aryan Gholizadeh(email: aryghm@gmail.com) has been activated in this group.\nUse /help to get a list of commands.\nBot's source code: https://github.com/AryanGHM/telegram-gp-bot"

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
    
    #set logging level to debug if debug is enabled.
    #set DEBUG to False if you want it disabled.
    if DEBUG:
        logging.basicConfig(level=logging.DEBUG)
    
    #recover chats from last run by their .grprf files
    SAVED_CHATS = local_files.recover_sess()
    
    for f, pref in SAVED_CHATS:
        CHATS.append(f)
        PREFERENCES[f] = pref
    
    #This function verifies that a channel is in CHATS whitelist or not
    #:param telethon.types.PeerChannel channel: the channel to verify
    async def verify_whitelist(channel):
        # get username of channel
        channel_name = (await bot(functions.channels.GetChannelsRequest([channel]))).chats[0].username
        if channel_name in CHATS:
            return True
        else:
            return False
    
    
    """ EVENTS """
    
    @bot.on(events.NewMessage(pattern="/maxwarn"))
    async def maxwarn(event):
         #Verify the input peer with whitelist
        if not (await verify_whitelist(event.to_id)):
            return
        #get argument from message
        max_warn = 0
        try:
            max_warn = int(str(event.raw_text).split(' ')[1])
        except ValueError:
            #failed to convert to int
            await event.reply("Please specify the maximum warnings count:\n/maxwarn __n__")
            return
        
        #forward
        channel_username = await gp_utils.get_channel_username(bot, event.to_id)
        
        await core.setmaxwarn(event, bot, PREFERENCES[channel_username], max_warn)     
        
    @bot.on(events.NewMessage(pattern="/help"))
    async def help(event):
        #Verify the input peer with whitelist
        if not (await verify_whitelist(event.to_id)):
            return
        
        #forward
        await core.showhelp(event, bot)    
    @bot.on(events.NewMessage(pattern="/unlockfwd"))
    async def uforward(event):
        #Verify the input peer with whitelist
        if not (await verify_whitelist(event.to_id)):
            return
        
        #forward 
        channel_username = await gp_utils.get_channel_username(bot, event.to_id)

        await core.unlockforward(event, bot, PREFERENCES[channel_username])         
        
    @bot.on(events.NewMessage(pattern="/unlocklnk"))
    async def ulink(event):
        #Verify the input peer with whitelist
        if not (await verify_whitelist(event.to_id)):
            return
        
        #forward 
        channel_username = await gp_utils.get_channel_username(bot, event.to_id)

        await core.unlocklink(event, bot, PREFERENCES[channel_username]) 
        
    @bot.on(events.NewMessage(pattern="/lockfwd"))
    async def lforward(event):
        #Verify the input peer with whitelist
        if not (await verify_whitelist(event.to_id)):
            return
        
        #forward 
        channel_username = await gp_utils.get_channel_username(bot, event.to_id)

        await core.lockforward(event, bot, PREFERENCES[channel_username]) 

    @bot.on(events.NewMessage(pattern="/locklnk"))
    async def llink(event):
        #Verify the input peer with whitelist
        if not (await verify_whitelist(event.to_id)):
            return
        
        #forward 
        channel_username = await gp_utils.get_channel_username(bot, event.to_id)

        await core.locklink(event, bot, PREFERENCES[channel_username])         
        
    @bot.on(events.NewMessage(pattern="/lockchat"))
    async def lchat(event):
        #Verify the input peer with whitelist
        if not (await verify_whitelist(event.to_id)):
            return
        
        #forward
        await core.lockchat(event, bot)
    
    @bot.on(events.NewMessage(pattern='/unlockchat'))
    async def uchat(event):
        #Verify the input peer with whitelist
        if not (await verify_whitelist(event.to_id)):
            return
        
        #forward
        await core.unlockchat(event, bot)
    
    @bot.on(events.NewMessage(pattern='/lockmedia'))
    async def lmedia(event):
        #Verify the input peer with whitelist
        if not (await verify_whitelist(event.to_id)):
            return
        
        #forward
        await core.lockmedia(event, bot)
    
    @bot.on(events.NewMessage(pattern='/unlockmedia'))
    async def umedia(event):
        #Verify the input peer with whitelist
        if not (await verify_whitelist(event.to_id)):
            return
        
        #forward
        await core.unlockmedia(event, bot)    
    
    @bot.on(events.NewMessage(pattern='/lockgif'))
    async def lgif(event):
        #Verify the input peer with whitelist
        if not (await verify_whitelist(event.to_id)):
            return
        
        #forward
        await core.lockgif(event, bot)
    
    @bot.on(events.NewMessage(pattern='/unlockgif'))
    async def ugif(event):
        #Verify the input peer with whitelist
        if not (await verify_whitelist(event.to_id)):
            return
        
        #forward
        await core.unlockgif(event, bot)  
        
    @bot.on(events.NewMessage(pattern='/locksticker'))
    async def lsticker(event):
        #Verify the input peer with whitelist
        if not (await verify_whitelist(event.to_id)):
            return
        
        #forward
        await core.locksticker(event, bot)    
        
    @bot.on(events.NewMessage(pattern='/unlocksticker'))
    async def usticker(event):
        #Verify the input peer with whitelist
        if not (await verify_whitelist(event.to_id)):
            return
        
        #forward
        await core.unlocksticker(event, bot)   

    @bot.on(events.NewMessage(pattern='/warn'))
    async def warn(event):
        #Verify the input peer with whitelist
        if not (await verify_whitelist(event.to_id)):
            return
        
        #forward 
        channel_username = await gp_utils.get_channel_username(bot, event.to_id)

        await core.warn(event, bot, PREFERENCES[channel_username]) 
        
    @bot.on(events.NewMessage(pattern='/dewarn'))
    async def dewarn(event):
        #Verify the input peer with whitelist
        if not (await verify_whitelist(event.to_id)):
            return
        
        #forward
        channel_username = await gp_utils.get_channel_username(bot, event.to_id)
        
        await core.dewarn(event, bot, PREFERENCES[channel_username]) 
    
    @bot.on(events.NewMessage(pattern='/ban'))
    async def ban(event):
        #Verify the input peer with whitelist
        if not (await verify_whitelist(event.to_id)):
            return
        
        #forward
        await core.ban(event, bot) 
        
    @bot.on(events.NewMessage(pattern='/unban'))
    async def unban(event):
        #Verify the input peer with whitelist
        if not (await verify_whitelist(event.to_id)):
            return
        
        #forward
        await core.unban(event, bot) 
        
    @bot.on(events.NewMessage())
    async def validate(event):
        #Verify the input peer with whitelist
        if not (await verify_whitelist(event.to_id)):
            return

        #forward 
        channel_username = await gp_utils.get_channel_username(bot, event.to_id)

        await core.validate(event, bot, PREFERENCES[channel_username])     
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
        
        #check if the group is already activated.
        if group_name in CHATS:
            await event.reply("The group is already activated!")
            return
        
        #Test for admin priviledges and send acknowledgements.
        self_status = httpmethods.get_chat_member_status(group_name, 
                                                      BOT_TOKEN.split()[0],
                                                      BOT_TOKEN)   #first segment of bot api token seperated by ':' is the bot user id     
        if "administrator" in self_status:
            await bot.send_message(group_name, ACTIVATION_ACKNOWLEDGE_MESSAGE)
            await event.reply("Done! I will send an acknowledge message in the group too.")
        else:
            await event.reply("Woops! Looks like I'm either not joined/promoted in the group!")        
            return
        
        CHATS.append(group_name)
        #Create a GroupPrefs class for the chat
        PREFERENCES[group_name] = local_files.GroupPrefs(group_name)
    
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
    