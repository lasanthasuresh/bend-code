from flask import Flask, request, jsonify
from flask_cors import CORS

from profit_calculator import calculate_profit
from service import load_all_data, load_data_of_company, get_price_data

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return 'This is my first API call!'


@app.route('/companies')
def all_companies():
    date = request.args.get('date')
    return jsonify(load_all_data(date))


@app.route('/company/<company>')
def get_company(company):
    date = request.args.get('date')
    return jsonify(load_data_of_company(company, date))


@app.route('/decisions/<company>')
def get_company_decisions(company):
    prices, decisions = get_price_data(company)
    return jsonify({
        'prices': prices,
        'decisions': decisions
    })


@app.route('/profit-calc/<company>')
def calc_profit_of_company(company):
    company_code = request.args.get('companyCode')
    from_date = request.args.get('fromDate')
    to_date = request.args.get('toDate')
    invested_amount = request.args.get('investedAmount')

    data = calculate_profit(company_code,from_date,to_date,float(invested_amount))
    print(data)

    return jsonify(data)
