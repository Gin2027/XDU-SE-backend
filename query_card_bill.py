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

import auth.wx
import json
from datetime import datetime


class bill:
    def __init__(self, time, place, type, amount):
        self.time = time
        self.place = place
        self.type = type
        self.amount = amount


def card_bill(start_date, end_date, id, password):
    bill_list = []
    try:
        ses = auth.wx.get_login_session(
            id, password)
        result = ses.post(
            auth.wx.BASE + 'infoCampus/playCampus/getAllPurposeCard.do',
            param={}
        ).json()
    except:
        return '查询失败!'
    if (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days <= 30:
        param = '{{\"startDate\":\"{}\",' + \
                '\"endDate\":\"{}\",' + \
                '\"offset\":1,' + \
                '\"cardNo\":null}}'
        param = param.format(datetime.strptime(start_date, "%Y-%m-%d").strftime(
            "%Y-%m-%d"), datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y-%m-%d"))
        result = ses.post(
            auth.wx.BASE + 'infoCampus/playCampus/getExpenseRecords.do', param=param).json()
        if len(result["expenseList"]) == 0:
            return "指定的时间段内没有消费记录。"
        for i in range(len(result["expenseList"])):
            obj = bill(result["expenseList"][i][4]["dataValue"], result["expenseList"][i][3]["dataValue"],
                       result["expenseList"][i][5]["dataValue"],
                       str(int(result["expenseList"][i][2]["dataValue"]) / 100))
            bill_list.append(obj.__dict__)
        return json.dumps(bill_list, ensure_ascii=False)
    else:
        return 1
