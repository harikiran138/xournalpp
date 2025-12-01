import time
import subprocess
import os
import signal
import threading
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from datetime import datetime
import uuid
import requests

# Configuration
RECORDING_DIR = os.path.abspath("backend/data/media/recordings")
THUMBNAIL_DIR = os.path.abspath("backend/data/media/thumbnails")
DB_API_URL = "http://localhost:5001/api/recordings" # Main backend URL

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

class RecorderService:
    def __init__(self):
        self.is_recording = False
        self.current_process = None
        self.current_recording_id = None
        self.start_time = None
        self.segment_index = 0
        self.output_pattern = ""

    def start_recording(self):
        if self.is_recording:
            return {"status": "error", "message": "Already recording"}

        self.current_recording_id = str(uuid.uuid4())
        self.start_time = time.time()
        self.segment_index = 0
        self.is_recording = True
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{self.current_recording_id}.mp4"
        filepath = os.path.join(RECORDING_DIR, filename)
        
        # Ensure directories exist
        os.makedirs(RECORDING_DIR, exist_ok=True)
        os.makedirs(THUMBNAIL_DIR, exist_ok=True)

        # FFMPEG Command Construction
        # Note: This is a platform-dependent command. 
        # For macOS (this environment), we use 'avfoundation'.
        # For Linux/X11 (ClassNova target), we would use 'x11grab' or 'kmsgrab'.
        
        system_platform = os.uname().sysname
        if system_platform == 'Darwin': # macOS
            # List devices: ffmpeg -f avfoundation -list_devices true -i ""
            # We'll assume input "1" or "0" for screen. Using "none" for audio for now to avoid permission issues in agent.
            cmd = [
                "ffmpeg",
                "-f", "avfoundation",
                "-i", "1:none", 
                "-r", "30",
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-pix_fmt", "yuv420p",
                filepath
            ]
        else: # Linux / Raspberry Pi
            cmd = [
                "ffmpeg",
                "-f", "x11grab",
                "-s", "1280x720",
                "-i", ":0.0+0,0",
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-crf", "23",
                filepath
            ]

        print(f"Starting recording with command: {' '.join(cmd)}")
        
        try:
            # Start ffmpeg process
            self.current_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid # Create new session group
            )
            
            # Notify Main Backend
            try:
                requests.post(DB_API_URL + "/", json={
                    "title": f"Recording {timestamp}",
                    "filepath": filepath,
                    "metadata": {"recording_id": self.current_recording_id}
                })
            except Exception as e:
                print(f"Failed to register recording with backend: {e}")

            socketio.emit('recording_started', {'id': self.current_recording_id})
            return {"status": "started", "id": self.current_recording_id, "file": filepath}
            
        except Exception as e:
            self.is_recording = False
            return {"status": "error", "message": str(e)}

    def stop_recording(self):
        if not self.is_recording or not self.current_process:
            return {"status": "error", "message": "Not recording"}

        try:
            # Send SIGTERM to the process group
            os.killpg(os.getpgid(self.current_process.pid), signal.SIGTERM)
            self.current_process.wait(timeout=5)
        except Exception as e:
            print(f"Error stopping process: {e}")
            # Force kill if needed
            try:
                os.killpg(os.getpgid(self.current_process.pid), signal.SIGKILL)
            except:
                pass

        duration = int(time.time() - self.start_time)
        self.is_recording = False
        self.current_process = None
        
        socketio.emit('recording_stopped', {'id': self.current_recording_id, 'duration': duration})
        
        # Update backend with duration (mock)
        # requests.patch(...) 

        return {"status": "stopped", "duration": duration}

    def get_state(self):
        return {
            "is_recording": self.is_recording,
            "recording_id": self.current_recording_id,
            "duration": int(time.time() - self.start_time) if self.is_recording else 0
        }

recorder = RecorderService()

@app.route('/api/recording/start', methods=['POST'])
def start():
    return jsonify(recorder.start_recording())

@app.route('/api/recording/stop', methods=['POST'])
def stop():
    return jsonify(recorder.stop_recording())

@app.route('/api/recording/state', methods=['GET'])
def state():
    return jsonify(recorder.get_state())

if __name__ == '__main__':
    print("🎥 Recording Daemon running on port 5002")
    socketio.run(app, host='0.0.0.0', port=5002)
