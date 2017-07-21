import telepot
import telepot.api
import urllib3


telepot.api._pools = {
    'default': urllib3.PoolManager(num_pools=3, maxsize=10, retries=5, timeout=120),
}

class Mailer:
    def __init__(self):
        self.key = ##"362753338:AAFXRClQnkiEBFqVXta245w_aMgqNtADUSc"
        pass

    def send(self,text):
        key = 
        self.bot = telepot.Bot(self.key)
        self.bot.sendMessage(238370268,text)

    def get_current_message(self):
        try:
            self.bot = telepot.Bot(self.key)
            updates = self.bot.getUpdates()
            if len(updates) == 0:
                return ""
            else:
                message_offset = updates[len(updates)-1]["update_id"]
                current_message = self.bot.getUpdates(offset = message_offset)
                return current_message[0]["message"]["text"]
        except:
            return ""
