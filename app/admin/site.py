from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from app.extensions import db
from app.decorators import admin_required
from sqlalchemy import func

bp = Blueprint('site', __name__)


@bp.route('/')
@login_required
@admin_required
def index():
    return render_template('admin/site/index.html')

