import pymysql
import json


def set_remind(form_dict):
    form_dict = json.loads(form_dict['json'])
    for key in form_dict:
        form_dict[key] = str(form_dict[key])
    db = pymysql.connect("api.ppoj.ac.cn", "ubuntu", "xdu-se-1603019", "remind")
    cursor = db.cursor()

    sql_select = "SELECT * FROM remind WHERE id = '%s'"% form_dict['androidID']
    print(sql_select)
    try:
        cursor.execute(sql_select)
        results = cursor.fetchall()
        print(results)
        if len(results) == 0:
            sql = "INSERT INTO remind VALUES ("
            sql += "'" + form_dict['androidID'] + "',"
            sql += "'" + form_dict['account'] + "',"
            sql += "'" + form_dict['cardpassword'] + "',"
            sql += "'" + form_dict['netaccount'] + "',"
            sql += "'" + form_dict['netpassword'] + "',"
            sql += "'" + form_dict['CampusNetworkLogin'] + "',"
            sql += "'" + form_dict['way1'] + "',"
            sql += "'" + form_dict['CampusNetworkBalance'] + "',"
            sql += "'" + form_dict['way2'] + "',"
            sql += "'" + form_dict['NetworkLimit'] + "',"
            sql += "'" + form_dict['CardBalance'] + "',"
            sql += "'" + form_dict['way3'] + "',"
            sql += "'" + form_dict['CardLimit'] + "',"
            sql += "'" + form_dict['Book'] + "',"
            sql += "'" + form_dict['way4'] + "',"
            sql += "'" + form_dict['email'] + "')"
            print(sql)
            cursor.execute(sql)
            db.commit()
        else:
            sql = "UPDATE remind SET "
            sql += "account='" + form_dict['account'] + "',"
            sql += "cardpassword='" + form_dict['cardpassword'] + "',"
            sql += "netaccount='" + form_dict['netaccount'] + "',"
            sql += "netpassword='" + form_dict['netpassword'] + "',"
            sql += "CampusNetworkLogin='" + form_dict['CampusNetworkLogin'] + "',"
            sql += "CampusNetworkLoginWay='" + form_dict['way1'] + "',"
            sql += "CampusNetworkBalance='" + form_dict['CampusNetworkBalance'] + "',"
            sql += "CampusNetworkBalanceWay='" + form_dict['way2'] + "',"
            sql += "NetworkLimit='" + form_dict['NetworkLimit'] + "',"
            sql += "CardBalance='" + form_dict['CardBalance'] + "',"
            sql += "CardBalanceWay='" + form_dict['way3'] + "',"
            sql += "CardLimit='" + form_dict['CardLimit'] + "',"
            sql += "Book='" + form_dict['Book'] + "',"
            sql += "email='" + form_dict['email'] + "',"
            sql += "BookWay='" + form_dict['way4'] + "' WHERE id = '%s'" % form_dict['androidID']
            print(sql)
            cursor.execute(sql)
            db.commit()
    except:
        db.rollback()
        print("Error")

    db.close()
    return "success"