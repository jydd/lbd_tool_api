from flask import jsonify, request, abort
from flask.views import MethodView
from app.extensions import db
from webargs.flaskparser import parser
from flask_login import current_user
from webargs import fields
from app.models.netease import Netease
from sqlalchemy import func
from app.models.netease_tasks import NeteaseTasks
from datetime import datetime
from sdk.netease.client import NeteaseClient


# 创建任务参数
parser_args = {
    'nid': fields.Int(required=True)
}

# 获取当前用户任务列表的参数
params_args = {
    'nid': fields.Int(required=True)
}

# 创建账号，修改账号参数
account_args = {
    'username': fields.Str(required=True),
    'password': fields.Str(required=True)
}


class NeteaseTasksAPI(MethodView):
    """获取网易云任务
    """
    def get(self):
        args = parser.parse(params_args, request, location='query')
        netease = Netease.query.filter_by(id=args['nid']).first()
        if netease is None:
            abort(404, '无此账号信息！')
        tasks = NeteaseTasks.query.filter_by(nid=netease.id).order_by(NeteaseTasks.id.desc()).all()

        return jsonify(success=True, data=[i.to_dict() for i in tasks[:10]])


class NeteaseLoginTaskAPI(MethodView):
    '''网易云登陆'''

    def post(self):
        """签到任务"""
        args = parser.parse(account_args, request, location='json')
        client = NeteaseClient(args['username'], args['password'])
        client.login()
        return jsonify(success=True, message='登陆成功')


class NeteaseSongTaskAPI(MethodView):
    '''网易云听歌任务'''

    def post(self):
        """签到任务"""
        args = parser.parse(parser_args, request, location='json')
        netease = Netease.query.filter_by(id=args['nid']).first()
        if netease is None:
            abort(404, '查不到此账号信息')

        # 限制一天只能触发一次签到
        if NeteaseTasks.query.filter(
                NeteaseTasks.nid == netease.id,
                NeteaseTasks.types == 2,
                func.date_format(NeteaseTasks.created_at, '%Y-%m-%d') ==
                datetime.now().strftime('%Y-%m-%d')).count():
            return {'success': False, 'message': '当天任务已提交！'}

        with db.auto_commit():
            task = NeteaseTasks(nid=netease.id, types=2, status=0)
            db.session.add(task)

        return jsonify(success=True, data=task.to_dict())


class NeteaseSignTaskAPI(MethodView):
    '''网易云签到任务'''

    def post(self):
        args = parser.parse(parser_args, request, location='json')
        netease = Netease.query.filter_by(id=args['nid']).first()
        if netease is None:
            abort(404, '查不到此账号信息')

        # 限制一天只能触发一次签到
        if NeteaseTasks.query.filter(
                NeteaseTasks.nid == netease.id,
                NeteaseTasks.types == 1,
                func.date_format(NeteaseTasks.created_at, '%Y-%m-%d') ==
                datetime.now().strftime('%Y-%m-%d')).count():
            return {'success': False, 'message': '当天任务已提交！'}

        client = NeteaseClient(netease.username, netease.password)
        res = client.sign()
        if res['code'] != 200:
            return jsonify(success=False, message=res['msg'])

        with db.auto_commit():
            task = NeteaseTasks(nid=netease.id, types=1, status=1, messages="签到成功")
            db.session.add(task)

        return jsonify(success=True, data=task.to_dict())


class NeteaseAccountInfoAPI(MethodView):

    def post(self):
        """获取当前账号网易云信息等级"""
        args = parser.parse(parser_args, request, location='json')
        netease = Netease.query.filter_by(id=args['nid']).first()
        if netease is None:
            abort(404, '账号不存在！')
        client = NeteaseClient(netease.username, netease.password)
        res = client.get_info()
        return jsonify(success=True, data=res)


class NeteaseAccountAPI(MethodView):
    """网易云账号管理
    获取账号列表
    创建账号
    """
    def post(self):
        """创建网易云账号"""
        args = parser.parse(account_args, request, location='json')

        model = Netease.query.filter_by(username=args['username']).first()

        if model is None:
            model = Netease(username=args['username'], password=args['password'])
            with db.auto_commit():
                db.session.add(model)

        if model.password != args['password']:
            with db.auto_commit():
                model.password = args['password']
                db.session.add(model)

        return jsonify(success=True, data=model.to_dict())

    def delete(self):
        '''获取当前用户下任务列表前10条
        参数指定的网易云ID
        '''
        args = parser.parse(params_args, request, location='query')
        netease = Netease.query.filter_by(id=args['nid']).first()
        if netease is None:
            abort(404, '无此账号信息！')
        tasks = NeteaseTasks.query.filter_by(nid=netease.id).all()

        with db.auto_commit():
            for item in tasks:
                db.session.delete(item)
            db.session.delete(netease)

        return jsonify(success=True, message="删除成功")
