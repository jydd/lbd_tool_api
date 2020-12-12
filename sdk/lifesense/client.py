from flask import abort
from hashlib import md5
import requests
import json
import time
import random


class LifesenseClient:
    def __init__(self, phone, pwd, step_num):
        self.phone = phone
        self.pwd = pwd
        self.step_num = step_num
        self.session = requests.session()
        self.user_agent = "Dalvik/2.1.0 (Linux; U; Android 9; SM-G9500 Build/PPR1.180610.011)"
        self.band_ids = [
            "http://we.qq.com/d/AQC7PnaOelOaCg9Ux8c9Ew95yumTVfMcFuGCHMY-",
            "http://we.qq.com/d/AQC7PnaOi9BLVrfJIiVTU8ENIbv_9Lmlqia1ToGc",
            "http://we.qq.com/d/AQC7PnaOXQhy3VvzFeP5bZMKmAQrGE6NJWdK3Xnk",
            "http://we.qq.com/d/AQC7PnaOaEXBdhkdXQvTRE1CO1fIqBuitbSSGt2r",
            "http://we.qq.com/d/AQC7PnaOdI9h0tfCr0KRlb78ISAE9qcaZ3btHrJE",
            "http://we.qq.com/d/AQC7PnaOsThRYksmQcvpa0klKFrupqaqKyEPm8nj",
            "http://we.qq.com/d/AQC7PnaOk8V-FV7R4ix61GToC5fh5I151hvlsNf6",
        ]
        self.token = self.get_token()

    def get_params(self):
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Accept-Encoding': 'gzip',
            'User-Agent': self.user_agent
        }
        data = {
            "password": md5(self.pwd.encode('utf-8')).hexdigest(),
            "clientId": md5(self.phone.encode('utf-8')).hexdigest(),
            "appType": 6,
            "loginName": self.phone,
            "timestamp": str(time.time()).replace('.', '')[0:13]
        }
        return headers, data

    def get_token(self):
        url = "https://sports.lifesense.com/sessions_service/login?systemType=1&version=4.6.8&platform=android"
        headers, data = self.get_params()
        res = self.session.post(url=url, data=json.dumps(data), headers=headers)
        res_json = res.json()

        if res_json['code'] != 200:
            abort(404, res['msg'])
        return res_json['data']

    def get_device_id(self):
        '''获得当前使用的设备'''
        url = 'https://sports.lifesense.com/sport_service/sport/sport/getActiveDevice?systemType=1&version=4.6.8'
        headers, data = self.get_params()
        res = self.session.post(url=url, data=json.dumps(data), headers=headers)
        res_json = res.json()
        device_id = res_json['data'].get('deviceId', None)
        if device_id is None:
            device_id = self.bind_device()

        return device_id

    def bind_device(self):
        '''绑定驱动设备'''
        bind_url = "https://sports.lifesense.com/device_service/device_user/bind"
        band_id = random.choice(self.band_ids)
        bind_data = json.dumps({"qrcode": band_id, "userId": int(self.token['userId'])})
        bind_header = {
            "Content-Type": "application/json; charset=utf-8",
            "Cookie": "accessToken=" + self.token['accessToken'],
            "User-Agent": self.user_agent
        }
        res = self.session.post(url=bind_url,
                                data=bind_data,
                                headers=bind_header)
        resp_data = res.json()

        if resp_data['code'] != 200:
            abort(403, resp_data['msg'])

        device_id = [i for i in resp_data['data']['deviceUserExts'] if i['isActive'] == 1][0]['deviceId']
        return device_id

    def _get_random_str(self, num):
        '''这是16位的随机字符串'''
        str_set = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        random_str = ""
        for i in range(num):
            index = random.randint(0, len(str_set) - 1)
            random_str += str_set[index]
        self.random_16_str = random_str

    def run(self):
        url = 'https://sports.lifesense.com/sport_service/sport/sport/uploadMobileStepV2?version=4.6.8&systemType=1'
        device_id = self.get_device_id()
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Cookie': 'accessToken=' + self.token['accessToken'],
        }
        cur_time = int(time.time())
        measurementTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(cur_time - (cur_time % 3600)))
        data = {
            "timestamp": str(time.time()).replace('.', '')[0:13],
            "list": [{
                "id": '468{}'.format(self._get_random_str(32)),
                "calories": str(int(self.step_num * 0.03)),
                "deviceId": device_id,
                "type": "0",
                "dataSource": "3",
                "userId": self.token['userId'],
                "priority": "0",
                "step": self.step_num,
                "created": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
                "distance": int(self.step_num * 0.74),
                "measurementTime": measurementTime
            }]
        }
        res = self.session.post(url=url, data=json.dumps(data), headers=headers)
        res_json = res.json()

        step_data = list(set(res_json['data']['pedometerRecordHourlyList'][0]['step'].split(",")))
        return max(step_data)


if __name__ == '__main__':
    # client = LifesenseClient('17305780556', 'a3940783', 1900)
    # client = LifesenseClient('15811100365', '111111', 8800)
    client = LifesenseClient('13282520400', 'a3940783', 12552)
    client.run()
    # client.get_token()
    # client.set_step()
    # zqy.run()
