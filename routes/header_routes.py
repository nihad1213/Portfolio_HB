#!/usr/bin/env python3

# Importing important modules
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, jsonify, session
from models.Chat import Chat
from models.User import User
from db import db
import uuid

# Create blueprint
headerRoutes = Blueprint('header_routes', __name__)

@headerRoutes.route('/schedule')
def schedule():
    return render_template('user/schedule.html')

@headerRoutes.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        user_id = session.get('user_id')
        print(f"GET request - User ID from session: {user_id}")  # Debug log
        
        if not user_id:
            print("User not authenticated")  # Debug log
            return jsonify({'error': 'User not authenticated'}), 401

        # If it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            receiver_id = request.args.get('receiver_id')
            print(f"AJAX request - Receiver ID: {receiver_id}")  # Debug log
            
            if not receiver_id:
                return jsonify({'success': True, 'messages': []})

            try:
                # Fetch chat messages
                chats = Chat.query.filter(
                    ((Chat.sender_id == user_id) & (Chat.receiver_id == receiver_id)) |
                    ((Chat.sender_id == receiver_id) & (Chat.receiver_id == user_id))
                ).order_by(Chat.created_at).all()

                chat_list = [
                    {
                        'message': chat.message,
                        'sender_id': chat.sender_id,
                        'receiver_id': chat.receiver_id,
                        'created_at': chat.created_at.isoformat(),
                    }
                    for chat in chats
                ]
                return jsonify({'success': True, 'messages': chat_list})
            except Exception as e:
                print(f"Error fetching messages: {str(e)}")  # Debug log
                return jsonify({'error': str(e)}), 500
        
        # Regular page load
        try:
            users = User.query.filter(User.id != user_id).all()
            print(f"Found {len(users)} other users")  # Debug log
            return render_template('user/chat.html', users=users)
        except Exception as e:
            print(f"Error loading users: {str(e)}")  # Debug log
            return jsonify({'error': str(e)}), 500

    elif request.method == 'POST':
        print("Received POST request")  # Debug log
        user_id = session.get('user_id')
        
        print(f"POST request - User ID from session: {user_id}")  # Debug log
        
        if not user_id:
            print("User not authenticated")  # Debug log
            return jsonify({'error': 'User not authenticated'}), 401

        try:
            data = request.get_json()
            print(f"Received data: {data}")  # Debug log
            
            if not data:
                print("No JSON data received")  # Debug log
                return jsonify({'error': 'Request data is missing'}), 400

            receiver_id = data.get('receiver_id')
            message = data.get('message')

            print(f"Receiver ID: {receiver_id}, Message: {message}")  # Debug log

            if not receiver_id or not message:
                print("Missing required fields")  # Debug log
                return jsonify({'error': 'Missing required fields'}), 400

            # Create new chat message
            chat = Chat(
                sender_id=user_id,
                receiver_id=receiver_id,
                message=message
            )
            db.session.add(chat)
            db.session.commit()

            print("Message saved successfully")  # Debug log

            return jsonify({
                'success': True,
                'chat': {
                    'message': chat.message,
                    'sender_id': chat.sender_id,
                    'receiver_id': chat.receiver_id,
                    'created_at': chat.created_at.isoformat(),
                }
            }), 201

        except Exception as e:
            print(f"Error in POST request: {str(e)}")  # Debug log
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
