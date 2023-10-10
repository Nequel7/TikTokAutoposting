import dotenv
from selenium import webdriver
import undetected_chromedriver as uc
import time
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import pickle
import pywinauto
from supports import random_proxy
from video_title import MARK, HASHTAGS

url = 'https://www.tiktok.com/'
dotenv.load_dotenv()


class BotPost:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--proxy-server=%s' % random_proxy())
        # self.options.add_argument(
        #     f'user-agent={os.getenv("USER_AGENT")}')
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--mute-audio")
        # self.browser = webdriver.Chrome(service=Service(
        #     executable_path=os.getenv('DRIVER_PATH')), options=self.options)
        self.browser = uc.Chrome(use_subprocess=False, driver_executable_path=os.getenv('DRIVER_PATH'),
                                 options=self.options)

    # close driver
    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    def load_video(self, account, i):
        filters = len(os.listdir('video'))
        videos_list = os.listdir('video')
        browser = self.browser
        # self.options.add_argument('--proxy-server=%s' % proxy[0])
        # with self.browser as browser:
        # browser = self.browser
        browser.get(url)
        browser.maximize_window()
        time.sleep(4)
        for cookie in pickle.load(
                open(f'{os.getenv("COOKIES_PATH")}{account}', 'rb')):
            browser.add_cookie(cookie)
        time.sleep(2)
        browser.refresh()
        time.sleep(2)
        browser.get('https://www.tiktok.com/creator-center/upload?from=upload')
        # browser.find_element(By.CSS_SELECTOR, "span[class='tiktok-y3rt08-SpanUploadText e18d3d946']").click()
        time.sleep(10)
        # iframe = WebDriverWait(browser, 20).until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, "iframe[data-tt='Upload_index_iframe']")))
        iframe = browser.find_element(By.CSS_SELECTOR, "iframe[data-tt='Upload_index_iframe']")
        browser.switch_to.frame(iframe)
        time.sleep(3)
        browser.find_element(By.TAG_NAME, "button").click()
        time.sleep(5)
        # load video
        app = pywinauto.application.Application()
        app.connect(title='Открытие')
        app.Dialog.Edit0.type_keys(
            f"{os.getenv('VIDEO_PATH')}{videos_list[i % filters]}",
            with_spaces=True)
        app.Dialog.Edit0.type_keys('{ENTER}')
        element = WebDriverWait(browser, 300).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='css-ug6w5y']"))).click()

        time.sleep(2)
        # set sound
        sound_input = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[class='jsx-3621125540 search-bar-input']")))
        sound_input.clear()
        sound_input.send_keys('1 second')
        sound_input.send_keys(Keys.ENTER)
        time.sleep(2)
        # move to 1 track in music list
        action = ActionChains(browser)
        action.move_to_element(sound_input).move_by_offset(xoffset=80,
                                                           yoffset=55).click().perform()
        time.sleep(2)
        play_btn = browser.find_element(By.CSS_SELECTOR,
                                        "div[class='jsx-1810555938 playButton']")
        # sound volume
        action.move_to_element(play_btn).move_by_offset(xoffset=-295,
                                                        yoffset=0).click().perform()
        sound_volume = \
            browser.find_elements(By.CSS_SELECTOR, "input[class='jsx-2730543169 scaleInput']")[-1]

        action.drag_and_drop_by_offset(source=sound_volume, xoffset=-69, yoffset=0).perform()
        time.sleep(1)
        # close video editor
        title = browser.find_element(By.CSS_SELECTOR, "span[class='jsx-366267946 modalTitle']")
        action.move_to_element(title).move_by_offset(xoffset=720,
                                                     yoffset=0).click().perform()
        time.sleep(2)
        # set mark
        title_video = browser.find_element(By.CSS_SELECTOR, "span[class='css-wpwnoe']")
        action = ActionChains(browser)
        action.move_to_element(title_video).move_by_offset(xoffset=590,
                                                           yoffset=36).click().perform()
        mark_input = WebDriverWait(browser, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input[class='jsx-2893442251 search-friends']")))
        mark_input.send_keys(MARK)
        time.sleep(2)
        mark_input.send_keys(Keys.ENTER)
        # set hashtag
        for hashtag in HASHTAGS:
            action = ActionChains(browser)
            action.move_to_element(title_video).move_by_offset(xoffset=500, yoffset=36).click().send_keys(
                f'#{hashtag}').perform()
            time.sleep(2)
            action.send_keys(Keys.ENTER).perform()

        time.sleep(1)
        browser.switch_to.window(browser.window_handles[0])
        # post video
        browser.execute_script("window.scrollBy(0,1200)")
        time.sleep(1)
        browser.switch_to.frame(iframe)

        browser.find_element(By.CSS_SELECTOR, "button[class='css-y1m958']").click()
        time.sleep(5)
        WebDriverWait(browser, 100).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div[class='tiktok-modal__modal-button is-highlight']")))
        print(f"✅ Video uploaded successfully in account ({account.split('_')[0]})")


class BotAuth:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument(
        #     f'user-agent={os.getenv("USER_AGENT")}')
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--mute-audio")
        # self.browser = webdriver.Chrome(service=Service(
        #     executable_path=os.getenv('DRIVER_PATH')), options=self.options)
        self.browser = uc.Chrome(use_subprocess=False, driver_executable_path=os.getenv('DRIVER_PATH'),
                                 options=self.options)

    def auth(self, username):
        with self.browser as browser:
            print('Auth starting...')
            browser.get(url)
            browser.maximize_window()
            time.sleep(3)
            # browser.find_element(By.ID, 'header-login-button').click()
            # time.sleep(3)
            # # browser.find_element(By.ID, 'loginContainer').find_element(By.LINK_TEXT,
            # #                                                            'Введите телефон / почту / имя пользователя').click()
            # browser.find_element(By.CSS_SELECTOR, "button[data-list-item-value='email/username']").click()
            # time.sleep(3)
            # # browser.find_element(By.LINK_TEXT, 'Войти через эл. почту или имя пользователя').click()
            # time.sleep(3)
            # # enter username
            # # tiktok-11to27l-InputContainer etcs7ny1
            # login_input = browser.find_element(By.CSS_SELECTOR,
            #                                    "input[class='tiktok-af1p2k-InputContainer etcs7ny1']")
            # login_input.clear()
            # login_input.send_keys(username)
            # time.sleep(2)
            # # enter password
            # # tiktok-wv3bkt-InputContainer etcs7ny1
            # password_input = browser.find_element(By.CSS_SELECTOR,
            #                                       "input[class='tiktok-15cv7mx-InputContainer etcs7ny1']")
            # password_input.clear()
            # password_input.send_keys(password)
            # time.sleep(3)
            # # press login btn
            # # e1w6iovg0 tiktok-11sviba-Button-StyledButton ehk74z00
            # browser.find_element(By.CSS_SELECTOR,
            #                      "button[class='ewv405f0 tiktok-186g1ag-Button-StyledButton ehk74z00']").click()
            # time.sleep(10)
            dm_btn = WebDriverWait(browser, 120).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-e2e='top-dm-icon']")))

            # insert cookie
            pickle.dump(
                browser.get_cookies(),
                open(f'C:/Users/zubri/PycharmProjects/autoposting/cookies/{username}_cookies', 'wb')
            )
            print('Cookies saved successfully !')
