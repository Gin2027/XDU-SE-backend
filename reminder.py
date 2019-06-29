import get_card_balance
import get_online_device
import get_pay_info
import get_unreturned_books
import requests
import pymysql
import re


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
        if user[10] == 'true' and user[11] == '1':
            cash = check_card_balance(user[1], user[2])
            if cash < float(user[12]):
                sql = "UPDATE remind SET CardBalance='false' WHERE id='%s'" % user[0]
                cursor.execute(sql)
                send_mail(user[15], "余额不足", ("当前余额为%s，低于您设置的额度 %s！" % (str(cash), user[12])))
                db.commit()
        
    db.close()


if __name__ == '__main__':
    remind()
