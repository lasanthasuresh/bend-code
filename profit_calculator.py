from enum import Enum

import date_utils
import service

COMMISSION = 0.00134

STATE_CASH_AT_HAND = 1
STATE_STOCKS_AT_HAND = 2

ACTION_BUY = 'buy'
ACTION_SELL = 'sell'


def to_dict(price_points):
    points = {}

    for point in price_points:
        points[point[0]] = point[1]

    return points


def do_buy(cash_at_hand, today_price):
    price_with_commission = today_price * (1 + COMMISSION)
    reminder = cash_at_hand % price_with_commission
    return (cash_at_hand - reminder) / price_with_commission, reminder


def do_sell(stocks_at_hand, today_price, remaining_cash=0):
    return stocks_at_hand * today_price * (1 - COMMISSION) + remaining_cash


def calculate_profit(companyCode, fromDate, toDate, invested_amount):
    price_points, decision_points = service.get_price_data(companyCode)

    fromDate = date_utils.to_epoch_date(fromDate)
    toDate = date_utils.to_epoch_date(toDate)

    price_points = to_dict(price_points)

    # decision_points = decision_points.sort(key=lambda x: x[0])

    invested = 0
    state = STATE_CASH_AT_HAND
    cash_at_hand = invested_amount
    stock_at_hand = 0
    worth = invested_amount

    for decision_point in decision_points:
        the_date = decision_point[0]
        the_action = decision_point[1]
        the_price = price_points[the_date]
        if fromDate <= the_date <= toDate:
            if state == STATE_CASH_AT_HAND:
                if the_action == ACTION_BUY:
                    stock_at_hand, cash_at_hand = do_buy(cash_at_hand, the_price)
                    state = STATE_STOCKS_AT_HAND
                    worth = stock_at_hand * the_price + cash_at_hand
                # else:
                #     raise AssertionError("Invalid Action")
            else:
                if the_action == ACTION_SELL:
                    cash_at_hand = do_sell(stock_at_hand, the_price, remaining_cash=cash_at_hand)
                    stock_at_hand = 0
                    worth = cash_at_hand
                    state = STATE_CASH_AT_HAND
                # else:
                #     raise AssertionError("Invalid Action")
    return {
        'stock_at_hand': stock_at_hand,
        'cash_at_hand': cash_at_hand,
        'final_worth': worth,
        'profit': worth - invested_amount,
        'profit_percentage': (worth-invested_amount)*100 /invested_amount
    }
