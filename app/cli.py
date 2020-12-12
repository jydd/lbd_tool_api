import click
from flask.cli import AppGroup
from app.models.user import User
from app.models.role import Role
from app.extensions import db


def register_cli(app):
    init_cli = AppGroup('init', short_help='初始化工作')
    app.cli.add_command(init_cli)

    @init_cli.command(short_help='生成管理员')
    @click.option('--username', default='admin', help='账号')
    @click.option('--password', default='123456', help='密码')
    def admin(username, password):
        if not Role.query.first():
            print('初始化角色')
            Role.init_role()

        if User.query.filter_by(username=username).first():
            raise '账号已经生成，不需要重复生成！'

        with db.auto_commit():
            user = User(username=username, status=100, role_id=2, password=password, nickname='江先生')
            db.session.add(user)
            click.echo('成功生成账号:{}, 密码:{}'.format(username, password))

    @init_cli.command(short_help='重置密码')
    @click.option('--username', help='账号')
    @click.option('--password', help='密码')
    def reset_password(username, password):
        user = User.query.filter(User.username == username).first()
        with db.auto_commit():
            user.password = password

        click.echo('账户密码重置成功')
