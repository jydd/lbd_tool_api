from flask import Blueprint
from app.extensions import cors, csrf
from .errors import register_errors
from .resources.netease import NeteaseTasksAPI, NeteaseAccountAPI, NeteaseAccountInfoAPI, NeteaseSignTaskAPI, NeteaseSongTaskAPI, NeteaseLoginTaskAPI


bp = Blueprint('api_v1', __name__)
cors.init_app(bp)
csrf.exempt(bp)


# 网易云任务
bp.add_url_rule('/netease/tasks', view_func=NeteaseTasksAPI.as_view('netease_tasks'), methods=['GET', 'POST'])
bp.add_url_rule('/netease/tasks/sign', view_func=NeteaseSignTaskAPI.as_view('netease_tasks_sign'), methods=['POST'])
bp.add_url_rule('/netease/tasks/song', view_func=NeteaseSongTaskAPI.as_view('netease_tasks_song'), methods=['POST'])

bp.add_url_rule('/netease/login', view_func=NeteaseLoginTaskAPI.as_view('netease_login'), methods=['POST'])
bp.add_url_rule('/netease/account/info', view_func=NeteaseAccountInfoAPI.as_view('netease_info'), methods=['POST'])

# 网易云账号,列表，创建
bp.add_url_rule('/netease/account', view_func=NeteaseAccountAPI.as_view('netease_account'), methods=['GET', 'POST', 'DELETE'])


register_errors(bp)
