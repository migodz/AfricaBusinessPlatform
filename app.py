from flask import Flask
import config
from extentions import db
from flask_migrate import Migrate
from models import *
from blueprints.user import bp as user_bp
from blueprints.company import bp as company_bp
from blueprints.chamber import bp as chamber_bp


app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(user_bp)
app.register_blueprint(company_bp)
app.register_blueprint(chamber_bp)

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()



