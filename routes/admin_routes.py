#!/usr/bin/env python3

from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_mail import Mail, Message
from datetime import datetime

# Create blueprint
adminRoutes = Blueprint('admin_routes', __name__)

@adminRoutes.route('/admin')
def admin_index():
    return render_template('admin/admin.index.html')