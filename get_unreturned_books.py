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

from auth.wx import get_login_session
import json


def book(id, password):
    book_list = []
    try:
        x = get_login_session(id, password)
        for i in x.post(
                'http://202.117.121.7:8080/oaCampus/library/getReturn.do',
                param={"offset": 1}
        ).json()['list']:
            item = '《' + i['title'] + '》' + '应当在' + i['returnDate'] + '之前还'
            book_list.append(item)
    except:
        return '查询失败!'
    return json.dumps(book_list, ensure_ascii=False)
