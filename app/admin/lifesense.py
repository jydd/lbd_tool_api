from flask import Blueprint, render_template, jsonify, request, redirect, url_for, current_app, flash, json, abort
from flask_login import login_required
from app.extensions import db
from app.models.netease import Netease
from app.models.netease_tasks import NeteaseTasks
from app.decorators import admin_required
from app.forms.netease import NeteaseForm
from app.forms.common import AjaxDeleteForm
from app.models.lifesense import Lifesense


bp = Blueprint('lifesense', __name__)


@bp.before_request
@login_required
@admin_required
def before_request():
    pass


@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)

    query = Lifesense.query.order_by(Lifesense.id.desc())

    pre_page = current_app.config['POST_PRE_PAGE']
    pagination = query.paginate(page, pre_page)
    return render_template('admin/lifesense/index.html',
                           model=pagination.items,
                           page=page,
                           pagination=pagination)


@bp.route('/delete/<int:id>')
def delete(id):
    model = Lifesense.query.get_or_404(id)
    model.delete(True)
    flash('删除成功', 'success')
    return redirect(request.referrer or url_for('lifesense.index'))


@bp.route('/ajax_delete', methods=['POST'])
def ajax_delete():
    form = AjaxDeleteForm()
    if form.validate_on_submit():
        for i in json.loads(form.ids.data):
            Lifesense.query.get_or_404(i).delete(True)
        flash('删除成功', 'success')

    if form.errors:
        flash(form.errors, 'danger')

    return jsonify({'success': True, 'message': '删除成功'})
