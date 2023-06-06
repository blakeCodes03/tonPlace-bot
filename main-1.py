import time
import json
import random
from selenium import webdriver
import urllib.request
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import undetected_chromedriver as uc
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

from upload_pic_request import upload_pic
from render_pic import render_new_pic

software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
user_agent_rotator = UserAgent(software_names=software_names,
                               operating_systems=operating_systems,
                               limit=100)
user_agent = user_agent_rotator.get_random_user_agent()

options = webdriver.ChromeOptions()
options.add_argument("--disable-extensions")
options.add_argument("--disable-popup-blocking")
options.add_argument("--profile-directory=Default")
options.add_argument("--disable-plugins-discovery")
options.add_argument("--incognito")
options.add_argument("--window_size = 1420,1080")
options.add_argument(f'user_agent={user_agent}')

service = Service(executable_path="C:/seleniumDrivers/chromedriver")
driver = uc.Chrome(options=options)
act = ActionChains(driver)
wait = WebDriverWait(driver, 90)
driver.set_script_timeout(60)

#  loads accounts.json file that contains login details
f = open('accounts.json', )
users = json.load(f)


class LocalStorage:  # to access local storage on browser to obtain token

    def __init__(self, driver):
        self.driver = driver

    def __len__(self):
        return self.driver.execute_script("return window.localStorage.length;")

    def items(self) :
        return self.driver.execute_script( \
            "var ls = window.localStorage, items = {}; " \
            "for (var i = 0, k; i < ls.length; ++i) " \
            "  items[k = ls.key(i)] = ls.getItem(k); " \
            "return items; ")

    def keys(self) :
        return self.driver.execute_script( \
            "var ls = window.localStorage, keys = []; " \
            "for (var i = 0; i < ls.length; ++i) " \
            "  keys[i] = ls.key(i); " \
            "return keys; ")

    def get(self, key):
        return self.driver.execute_script("return window.localStorage.getItem(arguments[0]);", key)


    def __getitem__(self, key) :
        value = self.get(key)
        if value is None :
          raise KeyError(key)
        return value



def get_token():  # function to obtain token from local storage
    storage = LocalStorage(driver)
    token = storage.get("token")
    with open("token_value.txt", "w") as f:
        f.write(token)


def post_image():
    get_token()
    upload_pic()


def solve_captcha():  # function to solve page's captcha using javascript
    captcha_script = '''
    
            function captchaSolve() {
            const reduceObjectToArray = (obj) => Object.keys(obj).reduce(function (r, k) {
                return r.concat(k, obj[k]);
        }, []);
        
        const client = ___grecaptcha_cfg.clients[0]
        let result = [];
        result = reduceObjectToArray(client).filter(c => Object.prototype.toString.call(c) === "[object Object]")
        
        result = result.flatMap(r => {
            return reduceObjectToArray(r)
        })
        
        result = result.filter(c => Object.prototype.toString.call(c) === "[object Object]")
        
        const reqObj = result.find( r => r.callback)
        reqObj.callback("${cap}")
        
        }
        captchaSolve()
            
    '''
    try:
        driver.execute_async_script(captcha_script)
    except exceptions.JavascriptException as e:
        print(e.message)


def like_post():
    # like posts feature
    try:
        user_first_post_like = driver.find_element(by=By.CSS_SELECTOR,
                                                   value="div.secondary > div.Button__icon > svg._like > path")  # find like button that hasn't been clicked in selected profile
    except:
        print("all User posts have been liked already")
    else:
        user_first_post_like.click()
        print("liked successful")
        time.sleep(randint(7, 10))


def search_other_user():

    # search other users feature
    WebDriverWait(driver, 60).until(EC.visibility_of_element_located(
        (By.CLASS_NAME, "App__desktop_menu")))  # wait till page fully loaded before action



    # this block selects random account from accounts.json file
    # to carry out search, follow, like feature
    random_user = users[0]  # random user selected
    random_user_id = random_user["userID"]  # id of the random user selected
    random_username = random_user["username"]  # username of the random user selected


    #  this block concatenates texts to form format of css selectors e.g('a[href^="/id312609"] > a')
    #  to select the particular user during the search process
    # search_result_selector_0 = "'"
    # search_result_selector_1 = 'a[href^="'
    # search_result_selector_2 = random_user_id + '"]'
    # search_result_selector_3 = " > a'"
    # search_result_selector = search_result_selector_0 + search_result_selector_1 + search_result_selector_2 + search_result_selector_3
    # print(search_result_selector)

    search_result_selector = f''' a[href^="{random_user_id}"] > a '''

    # search_menu = driver.find_element(by=By.CSS_SELECTOR,
    #                                   value='a[href^="/search"]')  # find search button on homepage menu
    # search_menu.click()
    search_menu = ''' "document.querySelector('a[href^="/search"]').click()" '''
    driver.execute_script(search_menu)
    time.sleep(randint(7, 10))
    solve_captcha()
    search_field_input = driver.find_element(by=By.CSS_SELECTOR,
                                             value="div.SearchInput__input > div.Input__wrapper > input.Input")
    search_field_input.send_keys(random_username)  # search field input from array of profile names of various accounts
    time.sleep(randint(10, 15))
    search_result = driver.find_element(by=By.CSS_SELECTOR,
                                        value=search_result_selector)  # find first result of the search
    search_result.click()

    #  loading user profile using userID in new tab
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "div.Button > div.Button__text")))  # wait till follow/message button visible on user's page
    print("found user successfully")

    #  follow feature
    try:
        follow_button = driver.find_element(by=By.CSS_SELECTOR,
                                            value="div.Profile__follow_wrap > div.default")  # find follow button on user's profile
    except:
        print("user has already been followed")
    else:
        follow_button.click()
    finally:
        like_post()




def main():

    #   login process
    driver.get('https://ton.place/')
    ton_place_url = driver.current_url
    driver.implicitly_wait(120)

    login_btn = driver.find_element(by=By.CSS_SELECTOR,
                                    value="div.quinary > div.Button__text")  # find login button on homepage
    login_btn.click()
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located(
        (By.CLASS_NAME, "AuthPopover")))
    time.sleep(randint(3, 5))
    # enter_email = driver.find_element(by=By.XPATH,
    #                                   value="/html/body/div[1]/div/div/div/div/div[4]/div[2]/div/div/div[2]/div[1]/div[2]/div[2]")  # find login through google option
    # enter_email.click()
    login_using_email = "document.querySelectorAll('div.Auth__socials > div')[1].click()"  # find login through google option
    driver.execute_script(login_using_email)

    user = random.choice(users)  # selects random user from accounts.json file

    WebDriverWait(driver, 30).until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="yDmH0d"]')))

    driver.find_element(by=By.ID, value='identifierId').send_keys(
        user["email"])  # for automatic login

    driver.find_element(by=By.CSS_SELECTOR,
                        value='#identifierNext > div > button > span').click()
    password_selector = "input[type='password']"

    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, password_selector)))

    driver.find_element(by=By.CSS_SELECTOR,
                        value=password_selector).send_keys(user["password"])  # for automatic login

    driver.find_element(by=By.CSS_SELECTOR,
                        value='#passwordNext > div > button > span').click()
    time.sleep(15)

    if "https://ton.place/" in ton_place_url:  # check if current url is ton.place url
        print("login successful")
        pass
    else:
        print(f"failed login attempt for" + user['email']) # raises error for failed login attempt
        driver.quit()
    try:
        post_image()
        search_other_user()
    except:
        print("error while searching other users")
    finally:
        render_new_pic()














if __name__ == '__main__':  # for security because of automated login
    main()
