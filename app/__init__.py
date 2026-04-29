from flask import Flask
from app.database import close_db

app = Flask(__name__)
app.config['SECRET_KEY'] = '12341234'

app.teardown_appcontext(close_db)

@app.cli.command('init-db')
def init_db_command():
    from app.database import init_db
    init_db()
    print('Database initialized')

from app import routes