"""
Utility functions used across all gp bot.
Author: Aryan Gholizadeh:aryghm@gmail.com
Project's github link: https://github.com/AryanGHM/telegram-gp-bot

"""
from telethon import TelegramClient, functions
from telethon.tl import types
from telethon.utils import resolve_id
import pysqlite3 as sql

WARNINGS_MAIN_TABLE = "warnings"

"""
Get username of a channel from it's peer (eg. Message.to_id)

:param)telethon.TelegramClient bot: A live telegram api client to use.

:param_telethon.types.PeerChannel channel: The channel to get username of

"""
async def get_channel_username(bot, channel):
    return (await bot(functions.channels.GetChannelsRequest([channel]))).chats[0].username

"""
Warning database functions, 
All warnings are stored in "warnings" table.In the format of:

user_id | warning_count

"""
def open_warning_db(path):
    conn = sql.connect(path)
    
    if conn:
        cursor = conn.cursor()
    else:
        raise RuntimeError("Could not connect to a db: " + path)
    
    cursor.execute(""" CREATE TABLE IF NOT EXISTS {}(
                                            user_id integer NOT NULL,
                                            warn_count integer
                                            );
                                            """.format(WARNINGS_MAIN_TABLE)
        )     
    
    return conn

def increase_warn(warn_db_path, user_id, count, max_warn):
    #count of warnings should not exceed max warning count
    #and should not be less than 0
    if count < 0:
        count = 0
    elif count > max_warn:
        count = max_warn
        
    conn = open_warning_db(warn_db_path)
    cur = conn.cursor()
    
    #update if there is already a row in the db for user
    cur.execute("SELECT * FROM {0} WHERE user_id={1}".format(WARNINGS_MAIN_TABLE, str(user_id)))
    rows = cur.fetchall()
    
    if len(rows) < 1:
        #create a row 
        sql = '''INSERT INTO {0}(user_id, warn_count) VALUES({1}, {2})'''.format(WARNINGS_MAIN_TABLE, str(user_id), str(count))
                
        cur.execute(sql)
        conn.commit()        
    elif len(rows) > 1:
        raise RuntimeError("The user {0} has more than one row in the {1} database".format(str(user_id), str(warn_db)))
    
    elif len(rows) == 1:
        #update the row
        warn_count = rows[0][1]
        
        #we are going to increase the value of warnings
        count += int(warn_count)
        if count > max_warn:
            count = max_warn
    
        sql = '''UPDATE {0}
             SET warn_count={2} WHERE user_id={1}'''.format(WARNINGS_MAIN_TABLE, str(user_id), str(count))
    
        cur.execute(sql)
        conn.commit()          

def decrease_warn(warn_db_path, user_id, count, max_warn):
    #count of warnings should not exceed max warning count
    #and should not be less than 0
    if count < 0:
        count = 0
    elif count > max_warn:
        count = max_warn
        
    conn = open_warning_db(warn_db_path)
    cur = conn.cursor()
    
    #update if there is already a row in the db for user
    cur.execute("SELECT * FROM {0} WHERE user_id={1}".format(WARNINGS_MAIN_TABLE, str(user_id)))
    rows = cur.fetchall()
    
    if len(rows) < 1:
        #create a row 
        sql = '''INSERT INTO {0}(user_id, warn_count) VALUES({1}, {2})'''.format(WARNINGS_MAIN_TABLE, str(user_id), "0")
                
        cur.execute(sql)
        conn.commit()        
    elif len(rows) > 1:
        #each user should only have 1 row in the db
        raise RuntimeError("The user {0} has more than one row in the {1} database".format(str(user_id), str(warn_db_path)))
    elif len(rows) == 1:
        #update the row
        warn_count = rows[0][1]
        
        #we are going to decrease the value of warnings
        count = int(warn_count) - count
        if count < 0:
            count = 0
    
        sql = '''UPDATE {0}
             SET warn_count={2} WHERE user_id={1}'''.format(WARNINGS_MAIN_TABLE, str(user_id), str(count))
    
        cur.execute(sql)
        conn.commit()         
    
def get_warn(warn_db_path, user_id):
    conn = open_warning_db(warn_db_path)
    cur = conn.cursor()
    
    #update if there is already a row in the db for user
    cur.execute("SELECT * FROM {0} WHERE user_id={1}".format(WARNINGS_MAIN_TABLE, str(user_id)))
    rows = cur.fetchall()
    
    #if there's no row in the db for the user it basically
    #doesn't have any warnings
    if len(rows) < 1:
        return 0
    elif len(rows) == 1:
        return rows[0][1]
    else:
        #if a user has more than 1 row in the db something went wrong
        raise RuntimeError("The user {0} has more than one row in the {1} database".format(str(user_id), str(warn_db_path)))

""" 
Get access hash of a channel from it's username

"""
async def get_access_hash(bot, channel_username):
    resp = await bot(functions.contacts.ResolveUsernameRequest(channel_username))
    return resp.chats[0].access_hash    

#delete a message with message_id from the channel that is specified channel_username
async def delete_message(bot, message_id, channel_username):
    #get channel's input peer with access hash and it's channel id 
    channel_id = resolve_id(await bot.get_peer_id(await bot.get_input_entity(channel_username)))[0]
    access_hash = await get_access_hash(bot, channel_username)
    
    channel_peer = types.InputPeerChannel(channel_id, access_hash)
    #create the request then send it
    request = functions.channels.DeleteMessagesRequest(channel_peer, [message_id])
    await bot(request)    

#ban a user by a message from him/her
async def ban_by_msg(msg):
    try:
        await bot.edit_permissions(await bot.get_input_entity(event.to_id),
                                                       await bot.get_input_entity(event.from_id), 
                                                       view_messages=False,
                                                       )    
        
        return True
    except Exception:
        return False