from app.forms import netease


def register_filter(app):
    @app.template_filter('netease_status')
    def netease_status(index):
        return netease.netease_status.get(index, '未设置')

    @app.template_filter('netease_tasks_types')
    def netease_tasks_types(index):
        return netease.netease_tasks_types.get(index, '未设置')

    @app.template_filter('netease_tasks_status')
    def netease_tasks_status(index):
        return netease.netease_tasks_status.get(index, '未设置')

    @app.template_filter('strftime')
    def datetime_strftime(time):
        if time is None:
            return '不能为空'
        return time

    @app.template_filter('audit_status_button')
    def audit_status_button(status):
        if status == 9:
            return 'secondary'
        elif status == 8:
            return 'danger'
        elif status == 7:
            return 'success'
        else:
            return 'secondary'

    @app.template_filter('user_status')
    def user_status(status):
        return '已审核' if status == 100 else '未审核'


    @app.template_filter('user_status_button')
    def user_status_button(status):
        if status == 100:
            return 'success'
        elif status == 101:
            return 'danger'
        else:
            return 'secondary'

    @app.template_filter('vote_status')
    def vote_status(status):
        return '正常投票' if status == 1 else '弃票'
 
