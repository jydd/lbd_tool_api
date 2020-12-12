from app.extensions import db
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime
from app.models.role import Role, Permission
from app.models.model_mixin import BaseMixin
from app.extensions import login_manager
from werkzeug.security import generate_password_hash, check_password_hash


# User model
class User(db.Model, UserMixin, BaseMixin):
    """status 101普通用户"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    nickname = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    status = db.Column(db.Integer, default=101)
    last_ip = db.Column(db.String(16))
    last_login_at = db.Column(db.DateTime, default=datetime.now)

    # 关联的角色
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', back_populates='users')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_role()

    def set_role(self):
        if self.role is None:
            self.role = Role.query.filter_by(name='User').first()

    @property
    def password(self):
        pass

    @login_manager.user_loader
    def user_loader(user_id):
        return User.query.get(user_id)

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 验证密码
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role.name == 'Administrator'

    # 查看是否有权限
    def can(self, permission_name):
        permission = Permission.query.filter_by(name=permission_name).first()
        return permission is not None and self.role is not None and permission in self.role.permissions

    def to_dict(self):
        data = {
            'id': self.id,
            'role': self.role.name,
            'role_nickname': self.role.nickname,
            'username': self.username,
            'nickname': self.nickname
        }
        return data

    @staticmethod
    def to_collection_dict(query, page, per_page=10):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            }
        }
        return data


class Guest(AnonymousUserMixin):
    @property
    def is_admin(self):
        return False

    def can(self, permission_name):
        return False


login_manager.anonymous_user = Guest
login_manager.login_view = 'auth.login'
login_manager.login_message = '需要登陆才能访问'
login_manager.login_message_category = 'warning'
