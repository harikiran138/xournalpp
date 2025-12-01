from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'novaboard_secret_key')

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///novaboard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db
db.init_app(app)

with app.app_context():
    db.create_all()

# Import Routes (Blueprints)
from routes.ai import ai_bp
from routes.sessions import sessions_bp
from routes.recordings import recordings_bp
from routes.models import models_bp
from routes.ai import ai_bp
from routes.storage import storage_bp
from routes.nova3d import nova3d_bp

app.register_blueprint(sessions_bp, url_prefix='/api/sessions')
app.register_blueprint(recordings_bp, url_prefix='/api/recordings')
app.register_blueprint(models_bp, url_prefix='/api/models')
app.register_blueprint(ai_bp, url_prefix='/api/ai')
app.register_blueprint(storage_bp, url_prefix='/api/v2')
app.register_blueprint(nova3d_bp, url_prefix='/api/nova3d')

@app.route('/')
def health_check():
    return jsonify({"status": "active", "service": "NovaBoard Backend", "version": "2.2.0"})

@app.route('/media/<path:filename>')
def serve_media(filename):
    return send_from_directory(os.path.join(app.root_path, 'data/media'), filename)

# --- WebSocket Events ---

@socketio.on('connect')
def handle_connect():
    print('Client connected:', request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected:', request.sid)

@socketio.on('join_session')
def handle_join(data):
    room = data.get('roomId')
    username = data.get('username')
    join_room(room)
    emit('user_joined', {'username': username, 'sid': request.sid}, room=room)
    print(f"User {username} joined room {room}")

@socketio.on('leave_session')
def handle_leave(data):
    room = data.get('roomId')
    username = data.get('username')
    leave_room(room)
    emit('user_left', {'username': username}, room=room)

@socketio.on('board_update')
def handle_board_update(data):
    """
    Broadcast board changes to all other users in the room.
    """
    room = data.get('roomId')
    # Broadcast to everyone in the room EXCEPT the sender
    emit('board_update', data, room=room, include_self=False)

@socketio.on('cursor_move')
def handle_cursor_move(data):
    """
    Broadcast cursor position to others.
    """
    room = data.get('roomId')
    emit('cursor_update', data, room=room, include_self=False)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    print(f"🚀 NovaBoard Backend running on port {port}")
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
