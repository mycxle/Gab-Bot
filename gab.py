from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
import sys
import os
import pyimgur

sleepy_time = 10
def s():
    sleep(sleepy_time)

IMGUR_ID = os.environ['IMGUR_ID']
im = pyimgur.Imgur(IMGUR_ID)
PATH = os.path.dirname(os.path.realpath(__file__)) +"/pic.png"

username = None
try:
    username = sys.argv[1]
except:
    username = os.environ['scrape']
print("User to scrape: " + username)
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
options.add_argument('window-size=1366x768')

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

def i():
    browser.save_screenshot(PATH)
    uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
    return str(uploaded_image.link)

browser.get(login_url)

s()
print("> at login page: " + browser.title)
s()

u = browser.find_element_by_css_selector("input#username")
u.send_keys(username)
p = browser.find_element_by_css_selector("input#password")
p.send_keys(password)
p.send_keys(Keys.ENTER)

print("> entered credentials and pressed enter: " + browser.title)
s()
print("are we logged in: " + browser.title)
s()

browser.get(scrape_url)
scraping_text = "Scraping new users.."
print(scraping_text, end="")
s()

old_index = 0
index = 0
scrape_num = 0

while True:
    scrape_num += 1
    print(".", end="")
    btns = browser.find_elements_by_css_selector("a.user-list__item__follow")[index:]
    index += len(btns)

    followed = False
    for b in btns:
        if b.text == "Follow":
            if followed == False:
                print("")
                followed = True
            try:
                browser.execute_script("arguments[0].click();", b)
                sleep_time = random.randint(int(sleepy_time/2), int(sleepy_time*1.5))
                print("Followed user, now sleeping for: " + str(sleep_time))
                sleep(sleep_time)
            except Exception as e:
                print("Error following user: " + str(e) + " " + i())

    if followed == True:
        print(scraping_text, end="")
        scrape_num = 0
    elif scrape_num >= 3:
        print("")
        print(scraping_text, end="")
        scrape_num = 0

    load_more = browser.find_element_by_css_selector("a.user-list__load span")
    load_more.click()
    s()
    htmlElem = browser.find_element_by_tag_name('body')
    htmlElem.send_keys(Keys.END)
    s()

    if index == old_index:
        break

    old_index = index 

browser.quit()
print("EOF")