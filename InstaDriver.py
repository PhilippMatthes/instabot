
from selenium import webdriver # For webpage crawling
from time import sleep
import time
from selenium.webdriver.common.keys import Keys # For input processing
from random import randint
import sys # For file path processing
import datetime # For timestamp
import pickle # For data management
import os

from Mailer import Mailer
from Config import Config



class Driver(object):
    def __init__(self):

        try:
            from xvfbwrapper import Xvfb
            self.headless_availability = True
        except ImportError as e:
            self.headless_availability = False
            print("Headless testing not available.")

        # Set up Telegram Message Client
        self.mailer = Mailer()

        # Set up virtual display
        try:
            if self.headless_availability:
                self.display = Xvfb()
                self.display.start()
        except OSError:
            self.headless_availability = False

        # Load history
        try:
            with open("log/followed_users_all_time.pickle","rb") as f:
                self.followed_accounts = pickle.load(f)
        except:
            with open("log/followed_users_all_time.pickle","wb") as f:
                self.followed_accounts = {}
                pickle.dump({},f)
        try:
            with open("log/followed_users.pickle","rb") as f:
                self.accounts_to_unfollow = pickle.load(f)
        except:
            with open("log/followed_users.pickle","wb") as f:
                self.accounts_to_unfollow = []
                pickle.dump([],f)


        self.username = input("Username: ")
        self.password = input("Password: ")

        # Final setup
        if self.headless_availability:
            self.browser = webdriver.PhantomJS()
        else:
            self.browser = webdriver.Chrome()
        self.browser.set_window_size(1980,1080)

    # Returns nicely formatted timestamp
    def timestamp(self):
        return time.strftime('%a %H:%M:%S')+" "

    def focus(self,element):
        self.browser.execute_script("arguments[0].focus();", element)

    # Checks if a user was followed already
    def user_followed_already(self, user):
        if user in self.followed_accounts:
            return True
        else:
            return False


    # Logs into Instagram automatically
    def login(self):

        self.mailer.send("Logging in.")
        print("Logging in.")
        self.browser.get(Config.start_url)
        sleep(5)

        if (self.browser.current_url == "https://www.instagram.com/"):
            return
        if (self.mailer.get_current_message() == "Pause"):
            self.mailer.send("Bot paused.")
            raise Exception("Bot paused.")
        if (self.mailer.get_current_message() == "Stop"):
            self.mailer.send("Bot stopped.")
            raise Exception("Bot stopped.")

        try:
            username_field = self.browser.find_element_by_name("username")
            username_field.send_keys(self.username)
            password_field = self.browser.find_element_by_name("password")
            password_field.send_keys(self.password)
            password_field.send_keys(Keys.RETURN)
            sleep(10)
            return
        except KeyboardInterrupt:
            return
        except:
            sleep(1)
            self.login()
            return

    # Comments on a picture
    def comment(self):
        sleep(3)
        query = Config.comments[randint(0,len(Config.comments)-1)]
        say = query.format(self.author(),Config.smileys[randint(0,len(Config.smileys)-1)])
        try:
            comment_field = self.browser.find_element_by_xpath(Config.comment_xpath)
            comment_field.send_keys(say)
            comment_field.send_keys(Keys.RETURN)
            self.mailer.send("Commented on "+str(self.author())+"s picture with: "+say+"\n")
            print("Commented on "+str(self.author())+"s picture with: "+say)
            sleep(1)
        except KeyboardInterrupt:
            return
        except:
            self.mailer.send("Comment field not found.\n")
            print("Comment field not found.")

    # Searches for a certain topic
    def search(self, query):
        self.mailer.send("Searching for "+query+".")
        print("Searching for "+query+".")
        self.browser.get("https://www.instagram.com/explore/tags/"+query+"/")

    # Checks for error which occurs when pictures are removed while
    # switching through
    def error(self):
        try:
            error_message = self.browser.find_element_by_xpath(Config.error_xpath)
            self.mailer.send("Page loading error.")
            print("Page loading error.")
            return True
        except KeyboardInterrupt:
            return
        except:
            return False

    # Selects the first picture in a loaded topic screen
    def select_first(self):
        try:
            pictures = self.browser.find_elements_by_xpath(Config.first_ele_xpath)
            first_picture = pictures[9]
            self.focus(first_picture)
            first_picture.click()
            return True
        except KeyboardInterrupt:
            return
        except:
            sleep(5)
            return False

    # Switches to the next picture
    def next_picture(self):
        try:
            sleep(1)
            next_button = self.browser.find_element_by_xpath(Config.next_button_xpath)
            next_button.click()
            return
        except KeyboardInterrupt:
            return
        except:
            self.browser.get(self.browser.current_url)
            sleep(1)
            if not self.error():
                self.select_first()
            return

    # Loads the authors name
    def author(self):
        try:
            author = self.browser.find_element_by_xpath(Config.author_xpath)
            return str(author.get_attribute("title"))
        except KeyboardInterrupt:
            return
        except:
            self.mailer.send("Author xpath not found.\n")
            print("Author xpath not found.")
            return ""

    # Checks if the post is already liked
    def already_liked(self):
        try:
            full = self.browser.find_element_by_xpath(Config.like_button_full_xpath)
            return True
        except:
            return False

    # Likes a picture
    def like(self, topic):
        count = 0
        while self.already_liked() and count < 10:
            self.mailer.send("Post already liked. Skipping.\n")
            print("Post already liked. Skipping.")
            self.next_picture()
            count = count + 1
            sleep(1)
        try:
            self.mailer.send("Liked picture/video by: "+self.author()+".\n")
            print("Liked picture/video by: "+self.author()+".")
            like_button = self.browser.find_element_by_xpath(Config.like_button_xpath)
            like_button.click()
            sneaksleep = randint(0,10) + Config.delay
            sleep(sneaksleep)
            return
        except KeyboardInterrupt:
            return
        except:
            sleep(Config.delay)
            self.search(topic)
            self.select_first()
            self.skip_recommended()
            self.like(topic)
            return

    # Unfollows a user
    def unfollow(self, name):
        self.browser.get("https://www.instagram.com/"+name+"/")
        sleep(3)
        try:
            unfollow_button = self.browser.find_element_by_xpath(Config.unfollow_xpath)
            unfollow_button.click()
            self.mailer.send("Unfollowed: "+name+".\n")
            print("Unfollowed: "+name)
            sleep(2)
        except KeyboardInterrupt:
            return
        except:
            self.mailer.send("Unfollow button not found.\n")
            print("Unfollow button not found.")
            sleep(1)

    # Follows a user
    def follow(self):
        sleep(3)
        try:
            follow = self.browser.find_element_by_xpath(Config.follow_xpath)
            follow.click()
            self.mailer.send("Followed: "+self.author()+"\n")
            print("Followed: "+self.author())
            with open("log/followed_users.txt", "wb") as userfile:
                pickle.dump(self.accounts_to_unfollow, userfile)
            self.accounts_to_unfollow.append(self.author())
            self.followed_accounts.update({self.author():self.timestamp()})
            with open("log/followed_users_all_time.txt", "wb") as userfile:
                pickle.dump(self.followed_accounts, userfile)
            sleep(Config.delay + randint(0,10))
        except:
            self.mailer.send("Follow button not found.\n")
            print("Follow button not found.")
            sleep(1)

    # Coordinates every function in an endless loop
    def like_follow_loop(self):
        self.login()
        while True:
            for topic_selector in range(len(Config.topics)-1):
                if (self.mailer.get_current_message() == "Exit" or self.mailer.get_current_message() == "Pause" or self.mailer.get_current_message() == "Stop"):
                    raise Exception('Breaking out of inner loop')
                # Config.open_unfollow_screen()
                # Config.unfollow_via_unfollow_screen()
                self.search(Config.topics[topic_selector])
                self.select_first()
                if (topic_selector % 7 == 0):
                    if (self.mailer.get_current_message() == "Exit" or self.mailer.get_current_message() == "Pause" or self.mailer.get_current_message() == "Stop"):
                        raise Exception('Breaking out of inner loop')
                    if not self.error():
                        self.comment()
                        self.next_picture()
                for likes in range(3):
                    sleep(1)
                    if (self.mailer.get_current_message() == "Exit" or self.mailer.get_current_message() == "Pause" or self.mailer.get_current_message() == "Stop"):
                        raise Exception('Breaking out of inner loop')
                    if not self.error():
                        self.like(Config.topics[topic_selector])
                        self.next_picture()
                for follows in range(3):
                    sleep(1)
                    if not self.error():
                        if (self.mailer.get_current_message() == "Exit" or self.mailer.get_current_message() == "Pause" or self.mailer.get_current_message() == "Stop"):
                            raise Exception('Breaking out of inner loop')
                        self.next_picture()
                        count = 0
                        sleep(3)
                        while self.user_followed_already(self.author()) and count < 10:
                            if (self.mailer.get_current_message() == "Exit" or self.mailer.get_current_message() == "Pause" or self.mailer.get_current_message() == "Stop"):
                                raise Exception('Breaking out of inner loop')
                            self.mailer.send(self.author()+" was followed already. Skipping picture.")
                            print(self.author()+" was followed already. Skipping picture.")
                            self.next_picture()
                            count = count + 1
                            sleep(1)
                        self.follow()
                self.mailer.send("Accounts to unfollow: " + str(len(self.accounts_to_unfollow)))
                print("Accounts to unfollow: " + str(len(self.accounts_to_unfollow)))
                if len(self.accounts_to_unfollow) > 50:
                    for unfollows in range(3):
                        if (self.mailer.get_current_message() == "Exit" or self.mailer.get_current_message() == "Pause" or self.mailer.get_current_message() == "Stop"):
                            raise Exception('Breaking out of inner loop')
                        this_guy = self.accounts_to_unfollow[0]
                        self.unfollow(this_guy)
                        del self.accounts_to_unfollow[0]
