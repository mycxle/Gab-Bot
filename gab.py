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
browser = None
for retry in range(5):
    try:
        #hmmm
        browser = webdriver.Chrome()
        break
    except:
        print("Failed to make webdriver, trying again in 3 seconds..")
        sleep(3)

browser.get(login_url)

sleep(30)
print("> at login page: " + browser.title)

u = browser.find_element_by_css_selector("input#username")
u.send_keys(username)
p = browser.find_element_by_css_selector("input#password")
p.send_keys(password)
p.send_keys(Keys.ENTER)

print("> entered credentials and pressed enter: " + browser.title)
sleep(30)
print("are we logged in: " + browser.title)

browser.get(scrape_url)
sleep(15)
print(browser.title)

error_count = 0
old_size = 0
index = 0
while error_count < 3:
    btns = browser.find_elements_by_css_selector("a.user-list__item__follow")
    current_size = len(btns)
    for i in range(index, current_size):
        b = btns[i]
        if b.text == "Follow":
            b.click()
            index = i
            sleep_time = random.randint(1, 10)
            print("Followed user, now sleeping for: " + str(sleep_time))
            sleep(sleep_time)

    load_more = browser.find_element_by_css_selector("a.user-list__load span")
    load_more.click()
    sleep(random.randint(1, 5))
    htmlElem = browser.find_element_by_tag_name('body')
    htmlElem.send_keys(Keys.END)
    sleep(random.randint(1, 5))

    print("Old size: " + str(old_size) + "\nCurrent size: " + str(current_size) + "\n-------")

    if old_size == current_size:
        error_count += 1
        print("ENCOUNTERED AN ERROR! SLEEPING FOR 1 MINUTE")
        sleep(60)
    else:
        error_count = 0
    old_size = current_size

browser.quit()

display.stop()