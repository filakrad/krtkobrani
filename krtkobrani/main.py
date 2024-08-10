from flask import Flask
from flask_login import LoginManager, current_user, AnonymousUserMixin
import logging
from logging.config import dictConfig

from krtkobrani.db import db
from krtkobrani.config import config
from krtkobrani import db_models

dictConfig(config["LOGGING"])

logging.info("Logging successfully configured.")

dbcfg = config["DB"]
db_uri = f'{dbcfg["DRIVER"]}://{dbcfg["USER"]}:{dbcfg["PASSWORD"]}@{dbcfg["ADDRESS"]}:{dbcfg["PORT"]}/{dbcfg["NAME"]}'

# create the app
app = Flask(__name__)
# configure
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config["SQLALCHEMY_POOL_SIZE"] = 10
app.config['SECRET_KEY'] = 'krtkobrani-je-velmi-tajne'
# initialize the app with the extension
db.init_app(app)
with app.app_context():
    db.create_all()

'''register all blueprints'''
from krtkobrani.endpoints.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)
from krtkobrani.endpoints.base import base as base_blueprint
app.register_blueprint(base_blueprint)
from krtkobrani.endpoints.logged import logged as logged_blueprint
app.register_blueprint(logged_blueprint)
from krtkobrani.endpoints.admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint)

'''configure loging into flask session'''
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
def anon():
    anonym = AnonymousUserMixin()
    anonym.is_admin = False
    return anonym
login_manager.anonymous_user = anon
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    logging.debug(f"load_user user_id: {user_id}")
    logging.debug(f"{db.engine.pool.status()}")
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return db.session.query(db_models.Team).filter_by(id=user_id).first()


if __name__ == "__main__":
    app.run()

