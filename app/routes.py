from app import app
from flask import request
import get_card_balance
import query_card_bill
import get_unreturned_books
import get_grades
import get_pay_info
import get_online_device
import remind


@app.route('/index')
def index():
    return "hello"


@app.route('/api/card_balance', methods=['POST'])
def search_card_balance():
    username = request.form.get('id')
    password = request.form.get("password")
    return get_card_balance.card_balance(username, password)


@app.route('/api/card_bill', methods=['POST'])
def search_bill_balance():
    username = request.form.get('id')
    password = request.form.get('password')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    result = query_card_bill.card_bill(start_date, end_date, username, password)
    if result == 1:
        return "查询时间跨度不能超过 30 天。"
    else:
        return result


@app.route('/api/book', methods=['POST'])
def search_book():
    username = request.form.get('id')
    password = request.form.get('password')
    return get_unreturned_books.book(username, password)


@app.route('/api/grades', methods=['POST'])
def search_grades():
    username = request.form.get('id')
    password = request.form.get('password')
    return get_grades.grades(username, password)


@app.route('/api/net_balance', methods=['POST'])
def search_zfw():
    username = request.form.get('id')
    password = request.form.get('password')
    return get_pay_info.info(username, password)


@app.route('/api/online_device', methods=['POST'])
def search_zfw_dev():
    username = request.form.get('id')
    password = request.form.get('password')
    return get_online_device.info(username, password)


@app.route('/api/remind_task', methods=['POST'])
def search_set_remind():
    return remind.set_remind(request.form.to_dict())
