#!/usr/bin/env python3

from flask import Blueprint, render_template

# Create blueprint
mainRoutes = Blueprint('main_routes', __name__)

@mainRoutes.route('/create-event')
def create_event():
    return render_template('main/create-event.html')

@mainRoutes.route('/eventss')
def events():
    return render_template('main/events.html')