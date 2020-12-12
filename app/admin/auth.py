from flask import current_app, Blueprint, render_template, flash, redirect, url_for, request, abort
from app.forms.login import LoginForm
from app.models.user import User
from app.extensions import db, flask_redis
from app.helpers import is_safe_url
from flask_login import login_user, logout_user
import time


bp = Blueprint('auth', __name__)


@bp.route('/paull_login', methods=['GET', 'POST'])
def paull_login():
    '''
    真实的登陆地址
    '''
    form = LoginForm()
    if form.validate_on_submit():

        # 定义redis锁定账号
        login_username = 'yzwyh_user_login_{}'.format(form.username.data)

        # 限制失败次数
        if flask_redis.exists(login_username) and int(flask_redis.get(login_username)) >= 3:
            # 设定30秒后过期, 重新计算
            flask_redis.expire(login_username, 30)
            abort(403, '账号锁定30分钟')

        user = User.query.filter_by(username=form.username.data).first()

        try:
            if user is None or not user.validate_password(form.password.data):
                abort(403, '账号或密码错误！')
            elif user.role_id != 2:
                abort(403, '没有权限，只有管理员才能登陆！')
            elif user.status != 100:
                abort(403, '账号未审核!')
        except Exception as e:
            flask_redis.incr(login_username)
            flash(e.description, 'warning')
        else:
            if login_user(user, remember=form.remember_me.data):
                flash('登陆成功!', 'success')
                current_app.logger.info('{}登陆成功'.format(form.username.data))
                user.last_ip = request.remote_addr
                db.session.commit()
                next_page = request.args.get('next')
                if is_safe_url(next_page):
                    return redirect(next_page or url_for('site.index'))

        return redirect(url_for('auth.paull_login'))

    return render_template('admin/auth/login.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    '''
    登陆陷阱
    '''
    form = LoginForm()
    if form.validate_on_submit():
        # 定义redis假的锁定账号
        login_username = 'yzwyh_false_user_login_{}'.format(form.username.data)

        # 限制失败次数
        if flask_redis.exists(login_username) and int(flask_redis.get(login_username)) >= 3:
            # 设定30秒后过期, 重新计算
            flask_redis.expire(login_username, 30)
            abort(403, '账号锁定30分钟')

        flash('账号或密码错', 'warning')
        flask_redis.incr(login_username)

        # 延时2秒
        time.sleep(2)

        current_app.logger.info('{}:陷阱登陆地址访问'.format(request.headers.get('X-Real-Ip', request.remote_addr)))

        return redirect(url_for('auth.login'))

    return render_template('admin/auth/login.html', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    flash('退出成功', 'success')
    return redirect(url_for('auth.login'))
