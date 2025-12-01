from flask import Blueprint, request, jsonify
from models import db, Model3D
import uuid
import os
import json
import requests
from werkzeug.utils import secure_filename
from datetime import datetime

models_bp = Blueprint('models', __name__)

UPLOAD_FOLDER = 'backend/data/media/models'
ALLOWED_EXTENSIONS = {'glb', 'gltf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@models_bp.route('/', methods=['GET'])
def list_models():
    models = Model3D.query.all()
    return jsonify([m.to_dict() for m in models])

@models_bp.route('/', methods=['POST'])
def upload_model():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Ensure directory exists
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        model_id = str(uuid.uuid4())
        new_model = Model3D(
            id=model_id,
            name=request.form.get('name', filename),
            filepath=file_path,
            metadata_json=json.dumps({})
        )
        
        db.session.add(new_model)
        db.session.commit()
        
        return jsonify(new_model.to_dict()), 201
    
    return jsonify({'error': 'File type not allowed'}), 400

@models_bp.route('/<model_id>', methods=['DELETE'])
def delete_model(model_id):
    model = Model3D.query.get_or_404(model_id)
    
    # Try to remove the file
    try:
        if os.path.exists(model.filepath):
            os.remove(model.filepath)
    except Exception as e:
        print(f"Error deleting file: {e}")
        
    db.session.delete(model)
    db.session.commit()
    return jsonify({'message': 'Model deleted'})

# Curated list of Open Source Educational Models
EXTERNAL_MODELS = [
    {
        "name": "DNA Molecule",
        "category": "Biology",
        "url": "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/BoomBox/glTF-Binary/BoomBox.glb", # Placeholder for DNA
        "thumbnail": "🧬"
    },
    {
        "name": "Neil Armstrong Spacesuit",
        "category": "History",
        "url": "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/DamagedHelmet/glTF-Binary/DamagedHelmet.glb", # Placeholder
        "thumbnail": "👨‍🚀"
    },
    {
        "name": "Duck (Physics Demo)",
        "category": "Physics",
        "url": "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/Duck/glTF-Binary/Duck.glb",
        "thumbnail": "🦆"
    },
    {
        "name": "Avocado",
        "category": "Biology",
        "url": "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/Avocado/glTF-Binary/Avocado.glb",
        "thumbnail": "🥑"
    }
]

@models_bp.route('/external', methods=['GET'])
def list_external_models():
    return jsonify(EXTERNAL_MODELS)

@models_bp.route('/import', methods=['POST'])
def import_model():
    data = request.json
    url = data.get('url')
    name = data.get('name')
    
    if not url or not name:
        return jsonify({'error': 'URL and name are required'}), 400
        
    try:
        # Download the file
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        filename = secure_filename(f"{name}.glb")
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        # Save to DB
        model_id = str(uuid.uuid4())
        new_model = Model3D(
            id=model_id,
            name=name,
            filepath=file_path,
            metadata_json=json.dumps({"source": "external", "original_url": url})
        )
        
        db.session.add(new_model)
        db.session.commit()
        
        return jsonify(new_model.to_dict()), 201
        
    except Exception as e:
        print(f"Import failed: {e}")
        return jsonify({'error': str(e)}), 500

@models_bp.route('/<model_id>/annotations', methods=['POST'])
def add_annotation(model_id):
    model = Model3D.query.get_or_404(model_id)
    data = request.json
    
    if not data or 'text' not in data or 'position' not in data:
        return jsonify({'error': 'Text and position required'}), 400
        
    metadata = json.loads(model.metadata_json) if model.metadata_json else {}
    annotations = metadata.get('annotations', [])
    
    new_annotation = {
        "id": str(uuid.uuid4()),
        "text": data['text'],
        "position": data['position'], # {x, y, z}
        "created_at": datetime.utcnow().isoformat()
    }
    
    annotations.append(new_annotation)
    metadata['annotations'] = annotations
    model.metadata_json = json.dumps(metadata)
    
    db.session.commit()
    
    return jsonify(new_annotation), 201
