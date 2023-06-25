from flask import Flask
from routes import stock_blueprint
from tables import db
import os

app = Flask(__name__)
app.register_blueprint(stock_blueprint)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/stocks.db'

db_dir = os.path.dirname(app.config['SQLALCHEMY_DATABASE_URI'][10:])
os.makedirs(db_dir, exist_ok=True)

db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
      db.drop_all()
      db.create_all()
    app.run(debug=True)