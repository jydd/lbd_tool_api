from flask import Blueprint, render_template, \
    current_app, request, flash, redirect, url_for
from flask_login import login_required
from app.models.user import User
from app.models.role import Role
from app.forms.user import UserForm, UserUpdateForm
from app.decorators import admin_required
from app.extensions import db

bp = Blueprint('users', __name__)


@bp.before_request
@login_required
@admin_required
def before_request():
    pass


@bp.context_processor
def make_template_context():
    return dict(role=Role.query.all())


@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pre_page = current_app.config['POST_PRE_PAGE']
    rid = request.args.get('rid', None, type=int)
    county = request.args.get('county', None, type=int)
    search = request.args.get('search', None)
    query = User.query.order_by(User.id.desc())
    if rid:
        query = query.filter(User.role_id == rid)
    if county:
        query = query.filter(User.county == county)
    if search:
        query = query.filter(User.username == search)
    pagination = query.paginate(page, pre_page)
    return render_template(
        'admin/users/index.html',
        model=pagination.items,
        page=page,
        pagination=pagination)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    form = UserForm()
    model = User()
    if model.save(form):
        flash('添加用户成功', 'success')
        return redirect(url_for('users.index'))
    return render_template('admin/users/create.html', form=form)


@bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    """TODO 用户更新，不能修改用户名"""
    form = UserUpdateForm()
    model = User.query.get_or_404(id)
    if model.save(form):
        flash('更新成功', 'success')
        return redirect(url_for('users.index'))
    form.load(model)
    return render_template('admin/users/update.html', form=form)


@bp.route('/delete/<int:id>')
def delete(id):
    user = User.query.get_or_404(id)
    if user.role.name == 'Administrator':
        flash('管理员不能删除', 'danger')
        return redirect(url_for('users.index'))
    user.delete(True)
    flash('删除成功!', 'success')
    return redirect(url_for('users.index'))


@bp.route('/status/<int:id>/<int:status>')
def status(id, status):
    model = User.query.get_or_404(id)

    if model.role.name == 'Administrator':
        flash('不能修改管理员信息!', 'danger')
        return redirect(request.referrer or url_for('user.index'))

    with db.auto_commit():
        model.status = status

    flash('操作成功', 'success')
    return redirect(request.referrer or url_for('user.index'))


@bp.route('/log')
def log():
    page = request.args.get('page', 1, type=int)
    pre_page = current_app.config['POST_PRE_PAGE']
    pagination = User.query.paginate(page, pre_page)
    return render_template(
        'admin/users/log.html',
        model=pagination.items,
        page=page,
        pagination=pagination)
