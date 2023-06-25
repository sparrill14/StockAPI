from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
    
class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    peratio = db.Column(db.Float, nullable=True)
    market_cap = db.Column(db.BigInteger, nullable=True)
    prices = db.relationship('StockPrice', backref='stock', lazy=True)

    def __repr__(self):
        return '<Stock %r>' % self.ticker

class StockPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)

    def __repr__(self):
        return '<StockPrice %r>' % self.id
