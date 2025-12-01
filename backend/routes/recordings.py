from flask import Blueprint, request, jsonify
from models import db, Recording, Section
import uuid
from datetime import datetime
import json
import os

recordings_bp = Blueprint('recordings', __name__)

@recordings_bp.route('/', methods=['GET'])
def list_recordings():
    recordings = Recording.query.order_by(Recording.created_at.desc()).all()
    return jsonify([r.to_dict() for r in recordings])

@recordings_bp.route('/', methods=['POST'])
def create_recording():
    data = request.json
    recording_id = str(uuid.uuid4())
    
    # In a real scenario, the daemon might create the file, but here we register the intent
    # or the daemon calls this endpoint to register the recording.
    new_recording = Recording(
        id=recording_id,
        title=data.get('title', f"Recording {datetime.now().strftime('%Y-%m-%d %H:%M')}"),
        filepath=data.get('filepath', ''), # Might be updated later
        metadata_json=json.dumps(data.get('metadata', {}))
    )
    
    db.session.add(new_recording)
    db.session.commit()
    
    return jsonify(new_recording.to_dict()), 201

@recordings_bp.route('/<recording_id>', methods=['PATCH'])
def update_recording(recording_id):
    recording = Recording.query.get_or_404(recording_id)
    data = request.json
    
    if 'title' in data:
        recording.title = data['title']
    if 'filepath' in data:
        recording.filepath = data['filepath']
    if 'duration' in data:
        recording.duration = data['duration']
    if 'thumbnail_path' in data:
        recording.thumbnail_path = data['thumbnail_path']
    if 'metadata' in data:
        recording.metadata_json = json.dumps(data['metadata'])
        
    db.session.commit()
    return jsonify(recording.to_dict())

@recordings_bp.route('/<recording_id>/sections', methods=['GET'])
def list_sections(recording_id):
    sections = Section.query.filter_by(recording_id=recording_id).order_by(Section.start_ms).all()
    return jsonify([s.to_dict() for s in sections])

@recordings_bp.route('/<recording_id>/sections', methods=['POST'])
def add_section(recording_id):
    recording = Recording.query.get_or_404(recording_id)
    data = request.json
    
    section_id = str(uuid.uuid4())
    new_section = Section(
        id=section_id,
        recording_id=recording_id,
        name=data.get('name', 'New Section'),
        start_ms=data.get('start_ms', 0),
        end_ms=data.get('end_ms'),
        notes=data.get('notes', ''),
        thumbnail_path=data.get('thumbnail_path'),
        ai_summary=data.get('ai_summary')
    )
    
    db.session.add(new_section)
    db.session.commit()
    return jsonify(new_section.to_dict()), 201

@recordings_bp.route('/sections/<section_id>', methods=['PATCH'])
def update_section(section_id):
    section = Section.query.get_or_404(section_id)
    data = request.json
    
    if 'name' in data:
        section.name = data['name']
    if 'start_ms' in data:
        section.start_ms = data['start_ms']
    if 'end_ms' in data:
        section.end_ms = data['end_ms']
    if 'notes' in data:
        section.notes = data['notes']
    if 'ai_summary' in data:
        section.ai_summary = data['ai_summary']
        
    db.session.commit()
    return jsonify(section.to_dict())
