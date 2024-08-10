from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
import logging
from functools import wraps

from krtkobrani.db_models import News, Team, Player
from krtkobrani.db import db

admin = Blueprint('admin', __name__)

def admin_required(func):
    """
    Modified login_required decorator to restrict access to admin group.
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin:        # zero means admin, one and up are other groups
            flash("You don't have permission to access this resource.", "warning")
            return redirect(url_for("base.index"))
        return func(*args, **kwargs)
    return decorated_view


@admin.route('/admin_index')
@login_required
@admin_required
def admin_index():
    return render_template('admin_index.html')