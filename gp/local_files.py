"""
Read and write to local temporary and persistence files, such as group preferences
or credential configuration files.
Author: Aryan Gholizadeh:aryghm@gmail.com
Project's github link: https://github.com/AryanGHM/telegram-gp-bot

"""
import configparser

#Load credential configureation file
credentials = configparser.ConfigParser()
if len(credentials.read('credentials.ini')) < 1:
    raise RuntimeError("No credential configuration file found, visit https://github.com/AryanGHM/telegram-gp-bot for more information.")

"""
Get api id from credentials.ini file

"""
def get_api_id():
    try:
        return int(credentials['API_CREDS']['API_ID'])
    except IndexError:
        raise RuntimeError("Invalid credential configuration file, visit https://github.com/AryanGHM/telegram-gp-bot for more information.")

"""
Get api hash from credentials.ini file

"""
def get_api_hash():
    try:
        return credentials['API_CREDS']['API_HASH']
    except IndexError:
        raise RuntimeError("Invalid credential configuration file, visit https://github.com/AryanGHM/telegram-gp-bot for more information.")

"""
Get bot token from credentials.ini file

"""
def get_bot_token():
    try:
        return credentials['BOT_CREDS']['BOT_TOKEN']
    except IndexError:
        raise RuntimeError("Invalid credential configuration file, visit https://github.com/AryanGHM/telegram-gp-bot for more information.")

