from flask import Blueprint, request
from datetime import datetime
from pricegenerators import generate_stock_prices_gaussian, generate_stock_prices_gbm
from tables import Stock, StockPrice, db
from random import normalvariate, uniform

stock_blueprint = Blueprint('stocks', __name__, url_prefix='/stocks')

stock_start_date = datetime(1970, 1, 1)
stock_end_date = datetime(2023, 6, 24)

@stock_blueprint.route('/<string:ticker>', methods=['GET'])
def get_stock(ticker):
    start_date_arg = request.args.get('start_date')
    end_date_arg = request.args.get('end_date')

    if start_date_arg is None:
        start_date = stock_start_date
    else:
        start_date = datetime.strptime(start_date_arg, '%Y-%m-%d')

    if end_date_arg is None:
        end_date = stock_end_date
    else:
        end_date = datetime.strptime(end_date_arg, '%Y-%m-%d')

    print(start_date, end_date)

    stock = Stock.query.filter_by(ticker=ticker).first()
    if not stock:
        return {'error': 'Stock not found'}, 404

    prices = StockPrice.query.filter(
        StockPrice.stock_id == stock.id,
        StockPrice.date.between(start_date, end_date)
    ).all()

    return {'prices': [{ 'date': price.date.strftime('%Y-%m-%d'), 'price': price.price } for price in prices]}

@stock_blueprint.route('/<string:ticker>', methods=['POST'])
def create_stock(ticker):
    name = ticker
    peratio = normalvariate(mu=23, sigma=1)
    market_cap = uniform(100000, 10000000)

    if not ticker:
        return {'error': 'No ticker provided'}, 400

    stock = Stock.query.get(ticker)
    if stock:
        return {'error': 'Stock already exists'}, 400

    stock = Stock(ticker=ticker, name=name, peratio=peratio, market_cap=market_cap)
    db.session.add(stock)
    db.session.commit()

    prices = generate_stock_prices_gbm(stock_start_date, stock_end_date)
    for date, price in prices.items():
        stock_price = StockPrice(date=date, price=price, stock_id=stock.id)
        db.session.add(stock_price)
        db.session.flush()

    db.session.commit()

    return {'message': 'Stock created'}, 201

@stock_blueprint.route('/<string:ticker>', methods=['DELETE'])
def delete_stock(ticker):
    stock = Stock.query.get(ticker)
    if not stock:
        return {'error': 'Stock not found'}, 404

    StockPrice.query.filter_by(ticker=ticker).delete()
    db.session.delete(stock)
    db.session.commit()

    return {'message': 'Stock deleted'}, 200