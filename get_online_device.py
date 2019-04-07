# Copyright (C) 2019 by the XiDian Open Source Community.
#
# This file is part of xidian-scripts.
#
# xidian-scripts is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# xidian-scripts is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with xidian-scripts.  If not, see <http://www.gnu.org/licenses/>.

import time
import bs4
import re
import requests
import pytesseract
import json
from PIL import Image
from io import BytesIO
from auth.GLOBAL import HEADER

BASE_URL = "https://pay.xidian.edu.cn"

PAY_INFO_URL = "/home"
LOGIN_URL = "/login"
MAX_TRY = 5


def make_data_and_cookies(ses, id, passwd):
    vcode = ''
    while len(vcode) is not 4:
        soup = bs4.BeautifulSoup(ses.get(BASE_URL).text, "lxml")
        img_url = BASE_URL + soup.find('img', id='loginform-verifycode-image').get('src')
        vcv = soup.find('input', type='hidden').get('value')
        img = Image.open(BytesIO(ses.get(img_url).content))
        img = img.convert('1')
        vcode = pytesseract.image_to_string(img, lang='ar', config='--psm 7 digits')
        print(vcode)
    return {
        "LoginForm[username]": id,
        "LoginForm[password]": passwd,
        "LoginForm[verifyCode]": vcode,
        "_csrf": vcv,
        "login-button": ""
    }


def get_info(ses):
    """retrieve the data using the cookies"""
    info_url = BASE_URL + PAY_INFO_URL
    ip_list = []
    filt = re.compile(r'>(.*)<')
    soup = bs4.BeautifulSoup(ses.get(info_url).text, 'lxml')
    tr_list = soup.find_all('tr')
    for tr in tr_list:
        td_list = bs4.BeautifulSoup(str(tr), 'lxml').find_all('td')
        if len(td_list) == 0:
            continue
        elif len(td_list) == 4:
            ip = filt.search(str(td_list[0])).group(1)
            online_time = filt.search(str(td_list[1])).group(1)
            used_t = filt.search(str(td_list[2])).group(1)
            if used_t == '':
                continue
            ip_list.append((ip, online_time, used_t))
        elif len(td_list) == 6:
            break
    return ip_list


def info(id, passwd):
    result = []
    return_info = []
    for tryCnt in range(MAX_TRY):
        ses = requests.session()
        ses.headers = HEADER
        data = make_data_and_cookies(ses, id, passwd)
        ses.post(BASE_URL + LOGIN_URL, data=data)  # login
        ses.get(BASE_URL)
        try:
            result = get_info(ses)
            break
        except:
            ses.close()
    ip_cnt = len(result)
    if ip_cnt != 0:
        for ip in result:
            return_info.append('ip 地址: %s , 上线时间 %s , 使用流量 %s' % ip)
    else:
        return '查询失败'
    return json.dumps(return_info, ensure_ascii=False)
