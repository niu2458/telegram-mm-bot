"""
Some of Telegram's httpapi methods are written here to be used
in other modules of gp.
Author: Aryan Gholizadeh:aryghm@gmail.com
Project's github link: https://github.com/AryanGHM/telegram-gp-bot

"""
import requests
import json
TELEGRAM_API_LINK = "https://api.telegram.org/bot"


"""
Get a user's status in a chat, more information: https://core.telegram.org/bots/api#getchatmember

:param_str chat_name: The targeted chat username with '@' prefix

:param_int user_id: The targeted user's integer id
 
:param_str bot_token: The bot token to use, to access the Telegram's
http api.

"""

def get_chat_member_status(chat_name, user_id, bot_token):
    request_url = TELEGRAM_API_LINK + bot_token + "/getChatMember" #the url to send request to
    
    #Chat username must not be empty
    if not len(chat_name):
        return
    
    #Chat's username must have '@' prefix
    if not chat_name.startswith("@"):
        chat_name = "@" + chat_name
    
    #The post data of the request consists a chat_id, which 
    #is chat username with '@' and a user_id which is the 
    #users int id.
    request_data = {"chat_id": chat_name,
                    "user_id": str(user_id)}
    
    jresp = requests.post(request_url, data=request_data).json() #Get the json dictionary format of the response
    
    if jresp["ok"] == True:
        return str(jresp["result"]["status"])

""" 
Check if the given user is admin or creator.

:param_str chat_name: The targeted chat username with '@' prefix

:param_int user_id: The targeted user's integer id
 
:param_str bot_token: The bot token to use, to access the Telegram's
http api.

"""
def is_member_admin(chat_name, user_id, bot_token):
    caller_status = get_chat_member_status(chat_name, user_id, bot_token) 
    
    if caller_status:
        if "creator" in caller_status:
            return True
        elif "administrator" in caller_status:
            return True
        else:
            return False
    