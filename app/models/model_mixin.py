from app.extensions import db
from flask import current_app


class BaseMixin(object):
    def save(self, form, commit=True, **kwargs):
        """保存数据
        kwargs 里面包含不需要验证直接附值，比如所属于哪个用户
        # TODO 争对不同的模块，出不出的提示，比如用户，文章，记录的的东西不一样
        """
        if form.validate_on_submit() and self._load(form):
            self.__dict__.update(kwargs)
            with db.auto_commit():
                db.session.add(self)
            return self

    def load(self, form):
        return self._load(form)

    def _load(self, form):
        """使用输入数据填充模型
        :params data flaskForm
        """
        for k, v in form.data.items():
            if hasattr(self, k) and k != 'id':
                if v == '':
                    continue

                if form.__dict__[k].type == 'SelectField' and v == 0:
                    setattr(self, k, None)
                else:
                    setattr(self, k, v)
        return True

    def delete(self, physics=False):
        """physics是否是物理删除
        如果是文章模型就设置为回收站
        其它类型删除物理
        """
        with db.auto_commit():
            if not physics:
                self.status = 0
            else:
                db.session.delete(self)
        current_app.logger.info('删除：{}'.format(self.id))
        return True
