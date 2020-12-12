from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from flask import current_app, flash
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_redis import FlaskRedis
from flask_cors import CORS
from contextlib import contextmanager
from wechatpy import WeChatClient


# 微信
# wechat_client = WeChatClient(Config.WECHAT_APPID, Config.WECHAT_SECRET)


# 小程序
program_client = WeChatClient('wxe4a025318879e79b', '6b30e95dd190f9741dc84c2f30fd9b66')


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
            flash('未执行成功，请联系管理员', 'danger')
            raise e


db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
csrf = CSRFProtect()
login_manager = LoginManager()
flask_redis = FlaskRedis(decode_responses=True)
