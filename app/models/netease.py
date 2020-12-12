from datetime import datetime
from app.models.model_mixin import BaseMixin
from app.extensions import db
import hashlib


class Netease(db.Model, BaseMixin):
    """网易云模型
    id: 索引
    mid: Member 用户ID
    username: 账号
    password: 密码
    status: 状态（1正常，0失败）
    created_at: 创建时间
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    status = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)

    tasks = db.relationship('NeteaseTasks', back_populates='netease')

    def to_dict(self):
        res_data = {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'created_at': self.created_at
        }
        return res_data

    @property
    def pwd(self):
        m = hashlib.md5()
        m.update(self.password.encode('utf-8'))
        return m.hexdigest()


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
