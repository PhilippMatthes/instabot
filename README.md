# Project Title

This is my Instagram Bot. It is not programmed nor structured very well. I just quickly wrote this down. So please keep this in mind. The main purpose of this bot is to programmatically follow, like, comment and unfollow on Instagram. If you have the time, help me refactoring this sloppy peace of software.

## Getting Started

You must use your own Telegram bot. It is used to control the instagram bot, in case there is something going wrong. Create your Telegram bot via the Telegram Botfather and note the Token. Make sure to start your bot so it is ready and running!

### Installing

Clone the git repository. 
```
git clone https://github.com/PhilippMatthes/instabot.git
```

Install the needed packages.
```
python3 -m pip install selenium
python3 -m pip install urllib3
python3 -m pip install telepot
```

Create a file in which the users you followed are stored. This will be refactored soon!
```
cd instabot
python3
import pickle
with open("followed_users_all_time.txt","wb") as f:
... pickle.dump([],f)
with open("followed_users.txt","rb") as f:
... pickle.dump([],f)
```

Then go into the "Mailer.py" File and insert your Telegram Bot Token into the self.key field. This will redirect the Mailer to your Telegram bot.
To modify the topics which are scraped by the bot, 

## Running the Bot

Make sure you are in the instabot directory.
```
cd instabot
```
Launch the bot and enter username and password as prompted.
```
python3 Main.py
```
The terminal window will clear. You now have to switch over to your Telegram bot and send him "Start". The bot will launch.



### Controlling the bot via Telegram

```
Start - Starts the bot in the initial phase
Stop - Terminates the bot. It will not be able to run again!
Pause - Pauses the bot.
Continue - Continues after pausing the bot.
```
