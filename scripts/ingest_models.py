import json
import os
import requests
import uuid
import sys
from datetime import datetime

# Add backend directory to path to import models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
from app import app
from models import db, Model3D

MANIFEST_PATH = os.path.abspath("backend/data/models_manifest.json")
MEDIA_ROOT = os.path.abspath("backend/data/media/models")

def ingest_models():
    print(f"🚀 Starting model ingestion from {MANIFEST_PATH}")
    
    with open(MANIFEST_PATH, 'r') as f:
        models_data = json.load(f)
        
    with app.app_context():
        for item in models_data:
            name = item['name']
            category = item['category']
            url = item['url']
            
            print(f"Processing: {name} ({category})")
            
            # Check if exists
            existing = Model3D.query.filter_by(name=name).first()
            if existing:
                print(f"  - Already exists, skipping.")
                continue
                
            # Create directory
            model_id = str(uuid.uuid4())
            model_dir = os.path.join(MEDIA_ROOT, category, model_id)
            os.makedirs(model_dir, exist_ok=True)
            
            # Download
            try:
                print(f"  - Downloading from {url}...")
                response = requests.get(url, stream=True)
                response.raise_for_status()
                
                filename = "model.glb"
                filepath = os.path.join(model_dir, filename)
                
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                # Mock LODs (just copy for now since we lack tools)
                # In production: run gltf-pipeline / blender here
                import shutil
                shutil.copy(filepath, os.path.join(model_dir, "model_high.glb"))
                shutil.copy(filepath, os.path.join(model_dir, "model_med.glb"))
                shutil.copy(filepath, os.path.join(model_dir, "model_low.glb"))
                
                # Create Meta JSON
                meta = {
                    "id": model_id,
                    "name": name,
                    "category": category,
                    "source": item['source'],
                    "license": item['license'],
                    "original_url": url,
                    "filesize": os.path.getsize(filepath),
                    "lod": {
                        "high": "model_high.glb",
                        "med": "model_med.glb",
                        "low": "model_low.glb"
                    }
                }
                
                with open(os.path.join(model_dir, "meta.json"), 'w') as f:
                    json.dump(meta, f, indent=2)
                    
                # DB Insert
                new_model = Model3D(
                    id=model_id,
                    name=name,
                    filepath=filepath,
                    metadata_json=json.dumps(meta)
                )
                db.session.add(new_model)
                db.session.commit()
                print(f"  - ✅ Ingested successfully.")
                
            except Exception as e:
                print(f"  - ❌ Failed: {e}")

    print("✨ Ingestion complete.")

if __name__ == "__main__":
    ingest_models()
