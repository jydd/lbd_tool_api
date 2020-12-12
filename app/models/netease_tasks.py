from datetime import datetime
from app.models.model_mixin import BaseMixin
from app.extensions import db

 
class NeteaseTasks(db.Model, BaseMixin):
    """网易云任务
    id: 索引
    nid: Netease用户ID
    types: 类型（签到|听歌） 
    messages: msg状态（账号密码错, 登陆成功状态)
    status: 状态(0:未开始，1:已完成，2:进行中, 3:异常)
    created_at: 创建时间
    """
    id = db.Column(db.Integer, primary_key=True)
    nid = db.Column(db.Integer, db.ForeignKey('netease.id'))
    types = db.Column(db.Integer)
    status = db.Column(db.Integer, default=0)
    messages = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)

    netease = db.relationship('Netease', back_populates='tasks')

    def to_dict(self):
        res_data = {
            'id': self.id,
            'nid': self.nid,
            'types': self.types,
            'messages': self.messages,
            'status': self.status,
            'created_at': self.created_at
        }
        return res_data

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
