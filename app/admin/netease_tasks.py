from flask import Blueprint, render_template, jsonify, request, redirect, url_for, current_app, flash, json
from flask_login import login_required
from app.extensions import db
from app.models.netease import Netease
from app.models.netease_tasks import NeteaseTasks
from app.decorators import admin_required
from app.forms.netease import NeteaseForm, NeteaseTasksForm
from app.forms.common import AjaxDeleteForm

bp = Blueprint('netease_tasks', __name__)


@bp.before_request
@login_required
@admin_required
def before_request():
    pass


@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    nid = request.args.get('id', None)

    query = NeteaseTasks.query.order_by(NeteaseTasks.id.desc())

    if nid:
        query = query.filter_by(nid=nid)

    pre_page = current_app.config['POST_PRE_PAGE']
    pagination = query.paginate(page, pre_page)
    return render_template('admin/netease/tasks.html',
                           model=pagination.items,
                           page=page,
                           pagination=pagination)


@bp.route('/create/<int:uid>', methods=['GET', 'POST'])
def create(uid):
    form = NeteaseTasksForm()
    model = NeteaseTasks()
    if model.save(form, uid=uid):
        flash('添加任务成功', 'success')
        return redirect(url_for('netease.index'))

    return render_template('admin/netease/tasks_form.html', form=form)


@bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = NeteaseTasksForm()
    model = NeteaseTasks.query.get_or_404(id)

    if model.save(form):
        flash('更新任务成功', 'success')
        return redirect(url_for('netease.index'))

    form.load(model)

    return render_template('admin/netease/tasks_form.html', form=form, model=model)


@bp.route('/delete/<int:id>')
def delete(id):
    NeteaseTasks.query.get_or_404(id).delete(True)
    flash('删除成功', 'success')
    return redirect(request.referrer or url_for('netease.index'))


@bp.route('/ajax_delete', methods=['POST'])
def ajax_delete():
    form = AjaxDeleteForm()
    if form.validate_on_submit():
        for i in json.loads(form.ids.data):
            NeteaseTasks.query.get_or_404(i).delete(True)
        flash('删除成功', 'success')

    if form.errors:
        flash(form.errors, 'danger')

    return jsonify({'success': True, 'message': '删除成功'})
