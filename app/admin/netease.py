from flask import Blueprint, render_template, jsonify, request, redirect, url_for, current_app, flash, json, abort
from flask_login import login_required
from app.extensions import db
from app.models.netease import Netease
from app.models.netease_tasks import NeteaseTasks
from app.decorators import admin_required
from app.forms.netease import NeteaseForm
from app.forms.common import AjaxDeleteForm


bp = Blueprint('netease', __name__)


@bp.before_request
@login_required
@admin_required
def before_request():
    pass


@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)

    query = Netease.query.order_by(Netease.id.desc())

    pre_page = current_app.config['POST_PRE_PAGE']
    pagination = query.paginate(page, pre_page)
    return render_template('admin/netease/index.html',
                           model=pagination.items,
                           page=page,
                           pagination=pagination)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    form = NeteaseForm()
    model = Netease()
    if model.save(form):
        flash('添加账号成功', 'success')
        return redirect(url_for('netease.index'))

    return render_template('admin/netease/form.html', form=form)


@bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = NeteaseForm()
    model = Netease.query.get_or_404(id)
    model.password = len(model.password) * '*'

    if model.save(form):
        flash('更新成功', 'success')
        return redirect(url_for('netease.index'))

    form.load(model)

    return render_template('admin/netease/form.html', form=form, model=model)


@bp.route('/delete/<int:id>')
def delete(id):
    model = Netease.query.get_or_404(id)

    if len(model.tasks):
        flash('当前有任务，不能删除账号!', 'danger')
    else:
        model.delete(True)
        flash('删除成功', 'success')
    return redirect(request.referrer or url_for('netease.index'))


@bp.route('/ajax_delete', methods=['POST'])
def ajax_delete():
    form = AjaxDeleteForm()
    if form.validate_on_submit():
        for i in json.loads(form.ids.data):
            model = Netease.query.get_or_404(i)
            if len(model.tasks):
                flash('当前有任务，不能删除账号!', 'danger')
            else:
                model.delete(True)
                flash('删除成功', 'success')

    if form.errors:
        flash(form.errors, 'danger')

    return jsonify({'success': True, 'message': '删除成功'})
