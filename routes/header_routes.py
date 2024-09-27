#!/usr/bin/env python3

# Importing important modules
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app


# Create blueprint
headerRoutes = Blueprint('header_routes', __name__)

@headerRoutes.route('/schedule')
def schedule():
    return render_template('schedule.html')

@headerRoutes.route('/profile')
def profile():
    return render_template('user_profile_page2.html')

@headerRoutes.route('/events')
def events():
    return render_template('events.html')

@headerRoutes.route('/chat')
def chat():
    return render_template('chat.html') 


