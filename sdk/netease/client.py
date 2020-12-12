from flask import abort
from app.config import basedir
from app.extensions import flask_redis
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
import execjs
import json
import os


class NeteaseClient:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.arg2 = "010001"
        self.arg3 = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
        self.arg4 = "0CoJUm6Qyw8W8jud"
        self.session = requests.session()
        self.csrf = None
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'origin': 'https://music.163.com',
            'Referer': 'https://music.163.com/',
            'Host': 'music.163.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        }
        self.set_requests_cookies()

    def get_browser(self):
        # options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        # self.browser = webdriver.Chrome(options=options)
        self.browser = webdriver.Remote(
            command_executor="http://selenium-hub:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.CHROME
        )
        self.wait = WebDriverWait(self.browser, 2)

    def login(self):
        '''登陆获取用户 cookies '''
        if flask_redis.hexists(f'user:{self.username}', 'cookies'):
            return True
        try:
            self.get_browser()
            self.browser.get('https://music.163.com/')
            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//a[text()='登录']/.."))).click()
            # 选择手机登陆方式
            self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[text()='选择其他登录模式']"))).click()
            # 勾选同意条款
            self.browser.find_element_by_xpath("//input[@id='j-official-terms']").click()
            # 点击手机登录
            self.browser.find_element_by_xpath("//a[@data-type='mobile']").click()
            # 在号码输入框输入号码
            self.browser.find_element_by_xpath("//input[@id='p']").send_keys(self.username)
            # 在密码输入框输入密码
            self.browser.find_element_by_xpath("//input[@id='pw']").send_keys(self.password)
            # 点击登录按钮
            self.browser.find_elements_by_xpath("//a[@data-action='login']")[1].click()
        except Exception:
            pass

        try:
            # 判断账号密码是否正确
            errors = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='j-err u-err']")))
            if errors:
                abort(403, errors.text)
        except NoSuchElementException:
            pass
        except TimeoutException:
            pass

        try:
            # 验证是否成功,成功则设置 cookies
            if self.wait.until(EC.presence_of_element_located((By.XPATH, "//em[text()='我的主页']"))):
                cookies = json.dumps(self.browser.get_cookies())
                flask_redis.hset(f'user:{self.username}', 'cookies', cookies)
                flask_redis.expire(f'user:{self.username}', 86400 * 2)
                return cookies
        except NoSuchElementException:
            abort(403, '查不到信息，登陆失败!')
        except TimeoutException:
            abort(403, '超时，登陆失败!')
        finally:
            self.browser.quit()

    def set_requests_cookies(self):
        """设置session cookies
        Args:
            cookies (dict): selenium cookies
        """
        redis_cookies = flask_redis.hget(f'user:{self.username}', 'cookies')
        if redis_cookies is None:
            redis_cookies = self.login()
        cookies = json.loads(redis_cookies)
        for cookie in cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])

        self.csrf = self.session.cookies['__csrf']

    def get_params(self, text):
        """加密text并获得请求字符串
        Args:
            text (str): 需要加密的字符串
        Returns:
            dict: aes, rsa后的参数
        """
        with open(os.path.join(basedir, 'sdk/netease/croe.js')) as f:
            js_code = f.read()
        ctx = execjs.compile(js_code)
        res = ctx.call('get_params', text, self.arg2, self.arg3, self.arg4)
        return {
            'params': res['encText'],
            'encSecKey': res['encSecKey']
        }

    def sign(self):
        '''
        签到
        '''
        sign_url = f'https://music.163.com/weapi/point/dailyTask?csrf_token={self.csrf}'
        payload = flask_redis.hget(f'user:{self.username}', 'sign')
        if payload is None:
            payload = json.dumps(self.get_params('{"type": 1}'))
            flask_redis.hset(f'user:{self.username}', 'sign', payload)
        res = self.session.post(sign_url, headers=self.headers, data=json.loads(payload))
        return res.json()

    def get_info(self):
        '''获取账号等级信息'''
        url = f'https://music.163.com/weapi/user/level?csrf_token={self.csrf}'
        payload = flask_redis.hget(f'user:{self.username}', 'level')
        if payload is None:
            data = json.dumps({'csrf_token': self.csrf})
            payload = json.dumps(self.get_params(data))
            flask_redis.hset(f'user:{self.username}', 'level', payload)

        res = self.session.post(url, headers=self.headers, data=json.loads(payload))
        return res.json()['data']
