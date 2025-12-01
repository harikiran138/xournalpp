from flask import Blueprint, request, jsonify
import uuid

sessions_bp = Blueprint('sessions', __name__)

# In-memory storage for demo purposes (Use DB in production)
active_sessions = {}

@sessions_bp.route('/create', methods=['POST'])
def create_session():
    """
    Create a new collaboration session.
    """
    session_id = str(uuid.uuid4())[:8] # Short ID
    active_sessions[session_id] = {
        "users": [],
        "elements": []
    }
    
    return jsonify({
        "sessionId": session_id,
        "message": "Session created successfully"
    })

@sessions_bp.route('/<session_id>', methods=['GET'])
def get_session(session_id):
    """
    Get session details.
    """
    if session_id in active_sessions:
        return jsonify(active_sessions[session_id])
    return jsonify({"error": "Session not found"}), 404
