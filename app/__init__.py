from flask import Flask
from app.database import close_db

app = Flask(__name__)
app.config['SECRET_KEY'] = '12341234'

app.teardown_appcontext(close_db)

from app import routes