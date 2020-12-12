from flask import Flask, request, jsonify, render_template
from app.config import config, basedir
from app.extensions import db, migrate, login_manager, csrf, flask_redis
from app.admin import users, site, auth, netease, netease_tasks
from app.apis.v1 import api
from flask_login import current_user
from app.cli import register_cli
from app.filter import register_filter
from logging.handlers import RotatingFileHandler
import os
import logging


def create_app(config_class=None):
    if config_class is None:
        config_class = os.getenv('FLASK_CONFIG', 'development')
    app = Flask(__name__)
    app.config.from_object(config[config_class])

    register_logging(app)
    register_buleprints(app)
    register_extensions(app)
    register_handle_error(app)

    register_cli(app)
    register_template_context(app)
    register_filters(app)

    return app


# 注册蓝本
def register_buleprints(app):
    app.register_blueprint(site.bp)
    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(users.bp, url_prefix='/users')
    app.register_blueprint(netease.bp, url_prefix='/netease')
    app.register_blueprint(netease_tasks.bp, url_prefix='/netease_tasks')

    app.register_blueprint(api.bp, url_prefix='/api')


# 注册扩展
def register_extensions(app):
    app.jinja_env.add_extension('jinja2.ext.do')
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    flask_redis.init_app(app)


# 注册过滤器
def register_filters(app):
    register_filter(app)


# 注册日志
def register_logging(app):
    app.logger.setLevel(logging.INFO)

    class RequestFormatter(logging.Formatter):
        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    request_formatter = RequestFormatter(
        '[%(levelname)s] [%(asctime)s] %(remote_addr)s requested %(url)s in %(module)s: %(message)s'
    )
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/bluelog.log'),
                                       maxBytes=10 * 1024 * 1024,
                                       backupCount=10)
    file_handler.setFormatter(request_formatter)
    file_handler.setLevel(logging.INFO)
    # if not app.debug:
    app.logger.addHandler(file_handler)


def register_handle_error(app):
    from sqlalchemy.exc import OperationalError

    @app.errorhandler(OperationalError)
    def _handel_operationa_error(e):
        return jsonify(success=False, message="数据库链接超时，请检查是否可连接！")

    @app.errorhandler(403)
    def _handle_403_error(e):
        return render_template('errors/403.html')


# 生成模板公共变量
def register_template_context(app):
    @app.context_processor
    def make_template_context():
        return dict(admin=current_user)
