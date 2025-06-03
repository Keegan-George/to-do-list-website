from os import getenv
from dotenv import load_dotenv
from flask import Flask
from extensions import db
from blueprints.home import home_bp
from blueprints.update import update_bp
from blueprints.delete import delete_bp

# retrieve environment variables
load_dotenv()


def create_app():
    # create flask app
    app = Flask(__name__)

    # configure SQLite database relative to app instance folder
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL", "sqlite:///todo.db")

    # initialize app with db extension
    db.init_app(app)

    # set secret key
    app.config["SECRET_KEY"] = getenv("SECRET_KEY")

    # create table schema in database
    with app.app_context():
        db.create_all()

    # register blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(update_bp, url_prefix="/update")
    app.register_blueprint(delete_bp, url_prefix="/delete")

    return app
