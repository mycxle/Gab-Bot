from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
import sys
import os
from pyvirtualdisplay import Display

display = Display(visible=0, size=(800, 600))
display.start()

username = sys.argv[1]
print(username)
scrape_url = "https://gab.ai/" + username + "/followers"

login_url = "https://gab.ai/auth/login"
username = os.environ['username']
password = os.environ['password']

CHROMEDRIVER_PATH = "/app/.chromedriver/bin/chromedriver"

chrome_bin = os.environ.get('GOOGLE_CHROME_BIN', "chromedriver")
options = webdriver.ChromeOptions()
options.binary_location = chrome_bin
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument('headless')
options.add_argument('window-size=1200x600')

browser = None

for retry in range(5):
    try:
        browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=options)
        break
    except:
        print("Failed to make webdriver, trying again in 1 minute..")
        sleep(60)

if not browser:
    print("Exiting program. Unable to create webdriver..")
    exit()

browser.get(login_url)

sleep(10)
print("> at login page: " + browser.title)

u = browser.find_element_by_css_selector("input#username")
u.send_keys(username)
p = browser.find_element_by_css_selector("input#password")
p.send_keys(password)
p.send_keys(Keys.ENTER)

print("> entered credentials and pressed enter: " + browser.title)
sleep(10)
print("are we logged in: " + browser.title)

browser.get(scrape_url)
sleep(15)
print(browser.title)

old_index = 0
index = 0
scraping_text = "Scraping new users.."
scrape_num = 0
print(scraping)
while True:
    scrape_num += 1
    print(".", end="")
    btns = browser.find_elements_by_css_selector("a.user-list__item__follow")[index:]
    index += len(btns)

    followed = False
    for b in btns:
        if b.text == "Follow":
            if not followed:
                print("")
            else:
                followed = True
            try:
                b.click()
                sleep_time = random.randint(1, 10)
                print("Followed user, now sleeping for: " + str(sleep_time))
                sleep(sleep_time)
            except Exception as e:
                print("Error following user: " + str(e))

    if followed or scrape_num >= 10:
        print(scraping_text)
        scrape_num = 0

    load_more = browser.find_element_by_css_selector("a.user-list__load span")
    load_more.click()
    sleep(random.randint(1, 5))
    htmlElem = browser.find_element_by_tag_name('body')
    htmlElem.send_keys(Keys.END)
    sleep(random.randint(1, 5))

    if index == old_index:
        break

    old_index = index 

browser.quit()

display.stop()