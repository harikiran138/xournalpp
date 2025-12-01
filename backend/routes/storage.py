from flask import Blueprint, request, jsonify, send_from_directory
import os
import json
import uuid

storage_bp = Blueprint('storage', __name__)

STORAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/scenes'))
os.makedirs(STORAGE_DIR, exist_ok=True)

@storage_bp.route('/post/', methods=['POST'])
def save_scene():
    try:
        data = request.get_data()
        scene_id = str(uuid.uuid4())
        
        filepath = os.path.join(STORAGE_DIR, f"{scene_id}.json")
        with open(filepath, 'wb') as f:
            f.write(data)
            
        return jsonify({"id": scene_id})
    except Exception as e:
        print(f"Save error: {e}")
        return jsonify({"error": str(e)}), 500

@storage_bp.route('/<scene_id>', methods=['GET'])
def get_scene(scene_id):
    try:
        return send_from_directory(STORAGE_DIR, f"{scene_id}.json")
    except Exception as e:
        return jsonify({"error": "Scene not found"}), 404
