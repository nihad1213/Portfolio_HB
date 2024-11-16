#!/usr/bin/env python3

# Importing important modules
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, jsonify, session
from models.Chat import Chat
from models.User import User
from db import db
from uuid import uuid4
# Create blueprint
headerRoutes = Blueprint('header_routes', __name__)

@headerRoutes.route('/schedule')
def schedule():
    return render_template('user/schedule.html')

@headerRoutes.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            receiver_id = request.args.get('receiver_id')
            if not receiver_id:
                return jsonify({'success': True, 'messages': []})

            try:
                chats = Chat.query.filter(
                    ((Chat.sender_id == user_id) & (Chat.receiver_id == receiver_id)) |
                    ((Chat.sender_id == receiver_id) & (Chat.receiver_id == user_id))
                ).order_by(Chat.created_at).all()

                chat_list = [{
                    'message': chat.message,
                    'sender_id': chat.sender_id,
                    'receiver_id': chat.receiver_id,
                    'created_at': chat.created_at.isoformat(),
                } for chat in chats]
                return jsonify({'success': True, 'messages': chat_list})
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        try:
            users = User.query.filter(User.id != user_id).all()
            return render_template('user/chat.html', users=users)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    elif request.method == 'POST':
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401

        try:
            # Get JSON data and print it for debugging
            data = request.get_json(force=True)  # force=True to ensure parsing
            print("Received data:", data)
            
            if not data:
                return jsonify({'error': 'No data received'}), 400

            receiver_id = data.get('receiver_id')
            message = data.get('message', '').strip()

            print(f"Processing - receiver_id: {receiver_id}, message: {message}")

            # Validate data
            if not receiver_id:
                return jsonify({'error': 'receiver_id is required'}), 400
            if not message:
                return jsonify({'error': 'message is required and cannot be empty'}), 400

            # Create chat with explicit values
            new_chat = Chat(
                id=str(uuid4()),
                sender_id=user_id,
                receiver_id=receiver_id,
                message=message,
            )

            print("Chat object before commit:", {
                'id': new_chat.id,
                'sender_id': new_chat.sender_id,
                'receiver_id': new_chat.receiver_id,
                'message': new_chat.message
            })

            # Add and commit
            db.session.add(new_chat)
            db.session.commit()

            return jsonify({
                'success': True,
                'chat': {
                    'id': new_chat.id,
                    'message': new_chat.message,
                    'sender_id': new_chat.sender_id,
                    'receiver_id': new_chat.receiver_id,
                    'created_at': new_chat.created_at.isoformat()
                }
            }), 201

        except Exception as e:
            db.session.rollback()
            print("Error creating chat:", str(e))
            print("Error type:", type(e))
            return jsonify({'error': str(e)}), 500