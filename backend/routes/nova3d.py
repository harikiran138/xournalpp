from flask import Blueprint, jsonify
import subprocess
import os

nova3d_bp = Blueprint('nova3d', __name__)

@nova3d_bp.route('/launch', methods=['POST'])
def launch_nova3d():
    try:
        # Path to the launcher script
        script_path = os.path.abspath('runFreeCAD.sh')
        
        # Execute the script
        subprocess.Popen(['/bin/bash', script_path])
        
        return jsonify({'message': 'Nova3D launch initiated'}), 200
    except Exception as e:
        print(f"Error launching Nova3D: {e}")
        return jsonify({'error': str(e)}), 500
