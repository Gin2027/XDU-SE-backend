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

import auth.ids
import json


class grade:
    def __init__(self, semester, lessons):
        self.semester = semester
        self.lessons = lessons


def grades(id, password):
    try:
        ses = auth.ids.get_login_session(
            'http://ehall.xidian.edu.cn:80//appShow', id, password)
        ses.get('http://ehall.xidian.edu.cn//appShow?appId=4768574631264620', headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        })
        querySetting = [
            {  # 学期
                'name': 'XNXQDM',
                'value': '2017-2018-2,2018-2019-1',
                'linkOpt': 'and',
                'builder': 'm_value_equal'
            }, {  # 是否有效
                'name': 'SFYX',
                'value': '1',
                'linkOpt': 'and',
                'builder': 'm_value_equal'
            }
        ]
        courses = {}
        for i in ses.post(
                'http://ehall.xidian.edu.cn/jwapp/sys/cjcx/modules/cjcx/xscjcx.do',
                data={
                    'querySetting=': json.dumps(querySetting),
                    '*order': 'KCH,KXH',  # 按课程名，课程号排序
                    'pageSize': 1000,  # 有多少整多少.jpg
                    'pageNumber': 1
                }
        ).json()['datas']['xscjcx']['rows']:
            if i['XNXQDM_DISPLAY'] not in courses.keys():
                courses[i['XNXQDM_DISPLAY']] = []
            courses[i['XNXQDM_DISPLAY']].append((i['XSKCM'].strip(), str(i['ZCJ']), str(i['XFJD'])))
    except:
        return '查询失败'
    grade_list = []

    for i in courses.keys():
        d = []
        for j in courses[i]:
            if j[2] == 'None':
                d.append(j[0] + ':' + j[1])
            else:
                d.append(j[0] + ':' + j[1] + ' (' + j[2] + ')')
        obj = grade(i, d)
        grade_list.append(obj.__dict__)
    return json.dumps(grade_list, ensure_ascii=False)
