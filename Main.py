from InstaDriver import Driver
from Mailer import Mailer
from time import sleep
import traceback
import sys
import os

if __name__=="__main__":

    os.makedirs("./log", exist_ok=True)

    session = Driver()
    mailer = Mailer()
    mailer.send("Instagram Bot started. Please send >>Start<< to start")
    while True:
        message = mailer.get_current_message()
        if (message == "Start" or message == "Continue"):
            try:
                session.like_follow_loop()
            except Exception as err:
                for frame in traceback.extract_tb(sys.exc_info()[2]):
                    fname, lineno, fn, text = frame
                error = "Error in "+str(fname)+" on line "+str(lineno)+": "+str(err)
                print(error)
                mailer.send(error)
                pass
            except KeyboardInterrupt:
                mailer.send("Keyboard Interrupt. Bot will exit now.")
                print("Exiting...")
                break
        else:
            if (message == "Stop" or message == "Exit"):
                mailer.send("Instagram Bot will exit now.")
                break
            sleep(1)
