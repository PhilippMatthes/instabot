
from selenium import webdriver # For webpage crawling
from time import sleep
import time
from selenium.webdriver.common.keys import Keys # For input processing
from random import randint
import sys # For file path processing
import datetime # For timestamp
import pickle # For data management
import os
from xvfbwrapper import Xvfb
from Mailer import Mailer


# Available terminal output colors (May not work for non-OSX systems)
# Usage: print(bcolors.OKBLUE+"Text in blue"+bcolors.ENDC)
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Available comments: the first {} is replaced with the username
# the second is replaced with a smiley. Note that UTF-8 smileys are only
# supported by Firefox driver which may corrupt some timed functionalities.
class Tell:
    comment = [ "Nice @{} {}","@{} cool {} ","Great style @{} {}","Amazing @{} {}",\
                "Awesome @{} {}","Fantastic @{} {}","@{} {}","Brilliant one @{} {}",\
                "Pretty nice @{} {}","Awesome feed @{} {}","I like your feed @{} {}",\
                "Top @{} {}", "Really cool works @{}! {}", "@{} Rad!!! {}",\
                "This is cool @{} {}", "Love this @{} {}", "Great @{}! {}", "Yeah @{} {}"]
    smiley = [  ":)",":D","=D","=)",";)",":)",":)",";D" ]

class Driver(object):
    def __init__(self):

        # Set up Telegram Message Client
        self.mailer = Mailer()

        # Set up virtual display for Raspberry Pi compatibility
        self.display = Xvfb()
        self.display.start()
        self.logpath = sys.path[0]+"/console.txt"
        open(self.logpath, 'w').close()

        # Load history
        with open("followed_users_all_time.txt","rb") as userfile_all_time:
            self.followed_accounts = pickle.load(userfile_all_time)
        with open("followed_users.txt","rb") as userfile:
            self.accounts_to_unfollow = pickle.load(userfile)

        # The following (xpath) classes need to be refreshed every now and then.
        # they define, where elements are located on Instagram. Sometimes,
        # classes are Changed (eg. "coreSpriteHeartOpen" to "coreSpriteLikeHeartOpen")
        # this results in vast amount of errors and needs to be corrected.
        self.first_ele_class = "_si7dy"
        self.sections_xpath = "//*[contains(@class, '_6jvgy')]"
        self.local_name_xpath = ".//a[@class='_4zhc5 notranslate _j7lfh']"
        self.local_button_xpath = ".//*[@class='_ah57t _6y2ah _i46jh _rmr7s']"
        self.following_xpath = "//*[contains(@class, '_s53mj')]"
        self.following_link = "https://www.instagram.com/snrmtths/following/"
        self.follow_xpath = "//*[contains(@class, '_qv64e _gexxb _4tgw8 _njrw0')]"
        self.unfollow_xpath = "//*[contains(@class, '_qv64e _t78yp _r9b8f _njrw0')]"
        self.comment_xpath = "//*[contains(@class, '_bilrf')]"
        self.error_xpath = "//*[contains(@class, 'error-container -cx-PRIVATE-ErrorPage__errorContainer')]"

        self.author_xpath = "//*[contains(@class, '_2g7d5 notranslate _iadoq')]"
        self.next_button_xpath = "//*[contains(@class, '_3a693 coreSpriteRightPaginationArrow')]"
        self.like_button_xpath = "//*[contains(@class, '_8scx2 coreSpriteHeartOpen')]"
        self.like_button_full_xpath = "//*[contains(@class, '_8scx2 coreSpriteHeartFull')]"

        self.username = input("Username: ")
        self.password = input("Password: ")

        # Clearing the command line
        os.system('clear')

        # Final setup
        self.topics = ["graphic","render","cartoon","daily","art","design","cinema4d","animation","cg","illustration"]
        self.delay = 30
        self.start_url = "https://www.instagram.com/accounts/login/"
        self.account_url = "https://www.instagram.com/"+self.username+"/"
        self.browser = webdriver.PhantomJS()
        self.browser.set_window_size(1980,1080)

    # Checks if a user was followed already
    def user_followed_already(self, user):
        if user in self.followed_accounts:
            return True
        else:
            return False

    # Returns nicely formatted timestamp
    def timestamp(self):
        return time.strftime('%a %H:%M:%S')+" "

    # Logs into Instagram automatically
    def login(self):
        self.mailer.send(self.timestamp()+"Logging in.")
        print(self.timestamp()+"Logging in.")
        self.browser.get(self.start_url)
        sleep(5)
        if (self.browser.current_url == "https://www.instagram.com/"):
            return
        if (self.mailer.get_current_message() == "Exit" or self.mailer.get_current_message() == "Pause" or self.mailer.get_current_message() == "Stop"):
            raise Exception('Breaking out of inner loop')
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
        query = Tell.comment[randint(0,len(Tell.comment)-1)]
        say = query.format(self.author(),Tell.smiley[randint(0,len(Tell.smiley)-1)])
        try:
            comment_field = self.browser.find_element_by_xpath(self.comment_xpath)
            comment_field.send_keys(say)
            comment_field.send_keys(Keys.RETURN)
            self.mailer.send(self.timestamp()+"Commented on "+str(self.author())+"s picture with: "+say+"\n")
            print(self.timestamp()+"Commented on "+str(self.author())+"s picture with: "+say)
            sleep(1)
        except KeyboardInterrupt:
            return
        except:
            self.mailer.send(self.timestamp()+"Comment field not found.\n")
            print(self.timestamp()+"Comment field not found.")

    # Searches for a certain topic
    def search(self, query):
        self.mailer.send(self.timestamp()+"Searching for "+query+".")
        print(self.timestamp()+"Searching for "+query+".")
        self.browser.get("https://www.instagram.com/explore/tags/"+query+"/")

    # Checks for error which occurs when pictures are removed while
    # switching through
    def error(self):
        try:
            error_message = self.browser.find_element_by_xpath(self.error_xpath)
            self.mailer.send(self.timestamp()+"Page loading error.")
            print(self.timestamp()+"Page loading error.")
            return True
        except KeyboardInterrupt:
            return
        except:
            return False

    # Selects the first picture in a loaded topic screen
    def select_first(self):
        try:
            first_picture = self.browser.find_element_by_class_name(self.first_ele_class)
            first_picture.click()
            return True
        except KeyboardInterrupt:
            return
        except:
            sleep(5)
            # if not self.error():
            #     self.select_first()
            return False

    # Switches to the next picture
    def next_picture(self):
        try:
            sleep(1)
            next_button = self.browser.find_element_by_xpath(self.next_button_xpath)
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

    # Skips recommended pictures
    def skip_recommended(self):
        for x in range(9):
            self.next_picture()

    # Loads the authors name
    def author(self):
        try:
            author = self.browser.find_element_by_xpath(self.author_xpath)
            return str(author.get_attribute("title"))
        except KeyboardInterrupt:
            return
        except:
            self.mailer.send(self.timestamp()+"Author xpath not found.\n")
            print(self.timestamp()+"Author xpath not found.")
            return ""

    # Checks if the post is already liked
    def already_liked(self):
        try:
            full = self.browser.find_element_by_xpath(self.like_button_full_xpath)
            return True
        except:
            return False

    # Likes a picture
    def like(self, topic):
        count = 0
        while self.already_liked() and count < 10:
            self.mailer.send(self.timestamp()+"Post already liked. Skipping.\n")
            print(self.timestamp()+"Post already liked. Skipping.")
            self.next_picture()
            count = count + 1
            sleep(1)
        try:
            self.mailer.send(self.timestamp()+"Liked picture/video by: "+self.author()+".\n")
            print(self.timestamp()+"Liked picture/video by: "+self.author()+".")
            like_button = self.browser.find_element_by_xpath(self.like_button_xpath)
            like_button.click()
            sneaksleep = randint(0,10) + self.delay
            sleep(sneaksleep)
            return
        except KeyboardInterrupt:
            return
        except:
            sleep(self.delay)
            self.search(topic)
            self.select_first()
            self.skip_recommended()
            self.like(topic)
            return

    # Depreciated
    def open_unfollow_screen(self):
        self.browser.get(self.account_url)
        sleep(2)
        following = self.browser.find_elements_by_xpath(self.following_xpath)
        for element in following:
            link = element.get_attribute("href")
            if (link == self.following_link):
                element.click()
        sleep(2)

    # Depreciated
    def unfollow_via_unfollow_screen(self):
        try:
            sections = self.browser.find_elements_by_xpath(self.sections_xpath)
        except:
            print("Sections not found.")
            return
        for element in sections:
            profile = element.find_element_by_xpath(self.local_name_xpath)
            link = profile.get_attribute("href")
            button = element.find_element_by_xpath(self.local_button_xpath)
            button.click()
            sleep(10)
        return

    # Unfollows a user
    def unfollow(self, name):
        self.browser.get("https://www.instagram.com/"+name+"/")
        sleep(3)
        try:
            unfollow_button = self.browser.find_element_by_xpath(self.unfollow_xpath)
            unfollow_button.click()
            self.mailer.send(self.timestamp()+"Unfollowed: "+name+".\n")
            print(self.timestamp()+"Unfollowed: "+name)
            sleep(2)
        except KeyboardInterrupt:
            return
        except:
            self.mailer.send(self.timestamp()+"Unfollow button not found.\n")
            print(self.timestamp()+"Unfollow button not found.")
            sleep(1)

    # Follows a user
    def follow(self):
        sleep(3)
        try:
            follow = self.browser.find_element_by_xpath(self.follow_xpath)
            follow.click()
            self.mailer.send(self.timestamp()+"Followed: "+self.author()+"\n")
            print(self.timestamp()+"Followed: "+self.author())
            with open("followed_users.txt", "wb") as userfile:
                pickle.dump(self.accounts_to_unfollow, userfile)
            self.accounts_to_unfollow.append(self.author())
            self.followed_accounts.update({self.author():self.timestamp()})
            # self.followed_accounts[self.author()] = self.timestamp()
            with open("followed_users_all_time.txt", "wb") as userfile:
                pickle.dump(self.followed_accounts, userfile)
            sleep(self.delay + randint(0,10))
        except:
            self.mailer.send(self.timestamp()+"Follow button not found.\n")
            print(self.timestamp()+"Follow button not found.")
            sleep(1)

    # Depreciated
    def unfollow_all(self):
        self.open_unfollow_screen()
        for name in self.accounts_to_unfollow:
            self.unfollow(name)
            sleep(10)
        del self.accounts_to_unfollow[:]

    # Coordinates every function in an endless loop
    def like_follow_loop(self):
        self.login()
        while True:
            for topic_selector in range(len(self.topics)-1):
                if (self.mailer.get_current_message() == "Exit" or self.mailer.get_current_message() == "Pause" or self.mailer.get_current_message() == "Stop"):
                    raise Exception('Breaking out of inner loop')
                # self.open_unfollow_screen()
                # self.unfollow_via_unfollow_screen()
                self.search(self.topics[topic_selector])
                self.select_first()
                self.skip_recommended()
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
                        self.like(self.topics[topic_selector])
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
                            self.mailer.send(self.timestamp()+self.author()+" was followed already. Skipping picture.")
                            print(self.timestamp()+self.author()+" was followed already. Skipping picture.")
                            self.next_picture()
                            count = count + 1
                            sleep(1)
                        self.follow()
                self.mailer.send(self.timestamp() + bcolors.OKBLUE + "Accounts to unfollow: " + str(len(self.accounts_to_unfollow)) + bcolors.ENDC)
                print(self.timestamp() + bcolors.OKBLUE + "Accounts to unfollow: " + str(len(self.accounts_to_unfollow)) + bcolors.ENDC)
                if len(self.accounts_to_unfollow) > 50:
                    for unfollows in range(3):
                        if (self.mailer.get_current_message() == "Exit" or self.mailer.get_current_message() == "Pause" or self.mailer.get_current_message() == "Stop"):
                            raise Exception('Breaking out of inner loop')
                        this_guy = self.accounts_to_unfollow[0]
                        self.unfollow(this_guy)
                        del self.accounts_to_unfollow[0]
