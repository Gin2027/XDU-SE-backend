from app import app
from flask import request
import get_card_balance
import query_card_bill
import get_unreturned_books
import get_grades

@app.route('/index')
def index():
    return "hello"

@app.route('/api/card_balance',methods = ['POST'])
def search_card_balance():
    id = request.form.get('id')
    password = request.form.get("password")
    return get_card_balance.card_balance(id,password)

@app.route('/api/card_bill',methods = ['POST'])
def search_bill_balance():
    id = request.form.get('id')
    password = request.form.get('password')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    result = query_card_bill.card_bill(start_date,end_date,id,password)
    if result == 1:
        return "查询时间跨度不能超过 30 天。"
    else:
        return result

@app.route('/api/book',methods = ['POST'])
def search_book():
    id = request.form.get('id')
    password = request.form.get('password')
    return get_unreturned_books.book(id,password)

@app.route('/api/grades',methods = ['POST'])
def search_grades():
    id = request.form.get('id')
    password = request.form.get('password')
    return get_grades.grades(id,password)