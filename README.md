# Telegram Group Police
Telegram Group Police Bot, group management assistant. No ads, No payment, No nothing.

Open source free group police bot with very basic functionalities, such as warning system, ban users, change permissions and ...

# Usage
**Requirements:**
1. A python 3 installation with pip, _3.6.9_ version is the best choice.

2. requests package, you can install this using pip.

3.(optional) virtualenv installation, this is extremely recommended.

Clone the repo: 
> git clone https://github.com/AryanGHM/telegram-gp-bot/

cd into repo's directory:
> cd telegram-gp-bot

A virtualenv with **python 3.6.9** interpreter is strongly recommended for best functionalities. Virtualenv documentation: https://virtualenv.pypa.io/en/latest/userguide/#usage

Setup telethon in the venv:
https://docs.telethon.dev/en/latest/basic/installation.html

Place your credentials in the _credentials.ini_ file located in the project's root directory. The credentials needed are _Telegram API hash_, _Telegram API ID_, _Your bot's token_. More at: https://docs.telethon.dev/en/latest/basic/signing-in.html

Finally in the project's root directory:
> python main.py

# Source code Documentation
To change the source code consider just looking at it, basically, events first land in _main.py_ and then they are forwarded to _gp.core_ module and finally from core module they are handled and forwarded to the desired module, wether it's _gp.actions_ or _gp.filtres_.

Here I'm just going to tell you where to go for each task, the code is indeed very well documented and can guide you through.

### gp.filters
_gp.filters_ module methods are called from _gp.core.validate_ method which is called when every new message is recieved, it checks if any of the filters have been set to True in order to forward the messsage object to the activated filter.

Filters are defined in **Group Preferences** which are handled by _gp.local_files.GroupPref_ class. Change the _GroupPref_ class in order to add/remove variables and values to/from Group Prefences files. Filters are values under [FILTER] section of 
Group Prefences files. As Group Prefences files are written in configuration files format, they are handled by _configparser_ module. Filters can be set to **_True_** or **_False_** which in the file are defined by **_1_** or **_0_**. 

### gp.actions
_gp.actions_ module handles all actions that are by the bot for example changing permissions or banning users etc. Actions are directly forwarded from _gp.core_ methods to _gp.actions_ methods, but you can manipulate with the event in the middle of pipeline in _gp.core_ module. Actions are always activated and the action methods will be always called when needed.

### gp.core
To add any functionalities to bot, the standard way is to first setup a decorator and a function for it in _main.py_ then forward the event to _gp.core_ module and from there forward it to a method in either _gp.actions_ or _gp.filters_ module.
so you need to create **3 functions** for each method to be added, one in _main.py_, another in _gp.core_ module and the last one in either _gp.actions_ or _gp.filters_ module. If you want access a GP (Group Prefences) handle of a chat you can easily fetch it from _PREFERENCES_ dictionary in _main.py_ by using the chat's name as key, so PREFERENCES[chat_name]. **Note:** always validate the incoming chat with CHATS list, the chat name must be in CHATS list you can do this by using _verify_whitelist_ function of _main.py_.
