#!/usr/bin/env python3

# Importing important modules
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app


# Create blueprint
userRoutes = Blueprint('user_routes', __name__)

@userRoutes.route('/login')
def login():
    return render_template('login.html')

@userRoutes.route('/register')
def register():
    return render_template('register.html')