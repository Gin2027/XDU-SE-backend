import get_card_balance
import get_online_device
import get_pay_info
import get_unreturned_books
import requests
import pymysql
import re
import json
import time


def send_mail(dest, subject, text):
    url = "http://api.sendcloud.net/apiv2/mail/send"
    API_USER = 'xdu_se'
    API_KEY = 'LUMnnVyFGviqhDZx'
    params = {
        "apiUser": API_USER,
        "apiKey": API_KEY,
        "to": dest,
        "from": "noreply@xduacm.club",
        "fromName": "西电生活全提醒",
        "subject": subject,
        "html": text
    }
    r = requests.post(url, data=params)
    print(r.text)


def check_card_balance(id, passwd):
    info = get_card_balance.card_balance(id, passwd)
    return float(re.search(r'([0-9]+\.[0-9]+)', info).group(0))








# id
# account
# cardpassword
# netaccount
# netpassword
# CampusNetworkLogin
# CampusNetworkLoginWay
# CampusNetworkBalance
# CampusNetworkBalanceWay
# NetworkLimit
# CardBalance
# CardBalanceWay
# CardLimit
# Book
# BookWay
# email

def check_net_balance(id, passwd):
    info = get_pay_info.info(id, passwd)
    if '不' in info:
        return 'F'
    else:
        print(info)
        tmp = re.search(r'剩余 ([0-9]+\.[0-9]*)([a-zA-Z])B', info)
        return tmp.group(1) + tmp.group(2)

def check_book(id, passwd):
    all_book = json.loads(get_unreturned_books.book(id, passwd))
    date = time.strftime("%Y %m %d %H %M %S", time.localtime()).split(' ')[:3]
    valid_book = []

    def cmp(y1, m1, d1, y2, m2, d2):
        if y1 == y2:
            if m1 == m2:
                return d1 < d2
            else:
                return m1 < m2
        else:
            return y1 < y2

    for book in all_book:
        ans = re.search(r'(.*)应当在([0-9]+)\-([0-9]+)\-([0-9]+)', book).groups()
        if cmp(ans[1], ans[2], ans[3], date[0], date[1], date[2]):
            continue
        else:
            valid_book.append(ans)
    return valid_book



def remind():
    db = pymysql.connect("api.ppoj.ac.cn", "ubuntu", "xdu-se-1603019", "remind")
    cursor = db.cursor()

    def fetch_all():
        sql = 'select * from remind'
        results = []
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                print(row)
        except:
            print("Error: unable to fetch data")
            db.close()
        return results

    users = fetch_all()
    for user in users:
        if user[10] == 'True' and user[11] == '1':
            try:
                cash = check_card_balance(user[1], user[2])
                if cash < float(user[12]):
                    sql = "UPDATE remind SET CardBalance='False' WHERE id='%s'" % user[0]
                    cursor.execute(sql)
                    send_mail(user[15], "余额不足", ("当前余额为%s，低于您设置的额度 %s！" % (str(cash), user[12])))
                    db.commit()
            except:
                sql = "UPDATE remind SET CardBalance='False' WHERE id='%s'" % user[0]
                cursor.execute(sql)
        if user[13] == 'True' and user[14] == '1':
            try:
                valid_book = check_book(user[1], user[2])
                if len(valid_book) != 0:
                    sql = "UPDATE remind SET Book='False' WHERE id='%s'" % user[0]
                    cursor.execute(sql)
                    text = ""
                    for book in valid_book:
                        text = text + '%s 应在 %s年%s月%s日 之前还<br>' % book
                    print(text)
                    send_mail(user[15], "还书提醒", text)
                    db.commit()
            except:
                sql = "UPDATE remind SET Book='False' WHERE id='%s'" % user[0]
                cursor.execute(sql)
        if user[7] == 'True' and  user[8] == '1':
            try:
                info = check_net_balance(user[3], user[4])
                if info[0] != 'F':
                    num = float(info[:-1])
                    if info[-1] == 'M':
                        num /= 1024.0
                    if user[9] == '500':
                        user[9] = '0.5'
                    if num < float(user[9]):
                        sql = "UPDATE remind SET NetworkLimit='False' WHERE id='%s'" % user[0]
                        cursor.execute(sql)
                        text = '当前校园网剩余流量为 %sB , 小于设定的阈值 %s GB' % (info, user[9])
                        # print(text)
                        send_mail(user[15], '流量提醒', text)
                else:
                    sql = "UPDATE remind SET NetworkLimit='False' WHERE id='%s'" % user[0]
                    cursor.execute(sql)
                    send_mail(user[15], '流量提醒失败', '翼讯为不限制流量套餐')
            except:
                sql = "UPDATE remind SET NetworkLimit='False' WHERE id='%s'" % user[0]
                cursor.execute(sql)
    db.close()


if __name__ == '__main__':
    # print(check_net_balance('16030199026', '090699'))
    remind()
