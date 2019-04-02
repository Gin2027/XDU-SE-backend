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
import requests
import pytesseract
from lxml import html
from PIL import Image
from io import BytesIO
from auth.GLOBAL import HEADER

BASE_URL = "https://pay.xidian.edu.cn"

PAY_INFO_URL = "/home"
LOGIN_URL = "/login"


def make_data_and_cookies(ses, id, passwd):
    vcode = ''
    while len(vcode) is not 4:
        doc = html.document_fromstring(ses.get(BASE_URL).text)
        vcode_link = doc.cssselect('form img')[0].get('src')
        vcv = doc.cssselect('input[name="_csrf"]')[0].get('value')
        img_url = BASE_URL + vcode_link
        img = Image.open(BytesIO(ses.get(img_url).content))
        img = img.convert('1')
        vcode = pytesseract.image_to_string(img, lang='ar', config='--psm 7 digits')
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
    s = ses.get(info_url).text
    doc = html.document_fromstring(s)
    result = doc.cssselect('tr[data-key="3"]')[0]
    used = result.cssselect('td[data-col-seq="3"]')[0].text
    rest = result.cssselect('td[data-col-seq="7"]')[0].text
    return used, rest


def info(id, passwd):
    while True:
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
            time.sleep(1)
    return "此月已使用流量 %s , 剩余 %s " % result
