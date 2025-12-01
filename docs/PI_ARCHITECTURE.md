# NovaBoard Complete Architecture
## ClassNova Smart Classroom System

---

## Executive Summary

NovaBoard is a complete smart-classroom software system designed to run on **Raspberry Pi 4/5** with **ClassNovaOS** (Linux Lite). It transforms any projector into an AI-powered interactive smart board with offline-first capabilities, cloud sync, and advanced teaching tools.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        NOVABOARD SYSTEM                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              UI LAYER (Electron Kiosk)                    │  │
│  │  ┌────────────┬──────────────┬─────────────┬───────────┐ │  │
│  │  │ Whiteboard │ Media Viewer │  Recording  │ Dashboard │ │  │
│  │  │   Canvas   │    (PDF/PPT) │   Control   │ & Settings│ │  │
│  │  └────────────┴──────────────┴─────────────┴───────────┘ │  │
│  │         React Frontend (Port: 3000)                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ▲                                  │
│                              │ IPC / REST API                   │
│                              ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │            NOVA ENGINE LAYER (Python)                     │  │
│  │  ┌────────────┬──────────────┬─────────────┬───────────┐ │  │
│  │  │ Canvas     │ Media        │  Recording  │    AI     │ │  │
│  │  │ Engine     │ Processor    │   Engine    │  Pipeline │ │  │
│  │  └────────────┴──────────────┴─────────────┴───────────┘ │  │
│  │  ┌────────────┬──────────────┬─────────────┬───────────┐ │  │
│  │  │ Sync       │ File         │  Class      │  Device   │ │  │
│  │  │ Scheduler  │ Manager      │  Manager    │  Control  │ │  │
│  │  └────────────┴──────────────┴─────────────┴───────────┘ │  │
│  │         Flask API Server (Port: 5000)                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ▲                                  │
│                              │ System Calls / GPIO              │
│                              ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         CLASSNOVAOS INTERFACE LAYER                       │  │
│  │  ┌────────────┬──────────────┬─────────────┬───────────┐ │  │
│  │  │ GPIO       │ Display      │  Audio/Video│  Network  │ │  │
│  │  │ Controller │ Manager      │  Drivers    │  Manager  │ │  │
│  │  └────────────┴──────────────┴─────────────┴───────────┘ │  │
│  │         Linux Services & Drivers                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ▲                                  │
│                              │ Hardware I/O                     │
│                              ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              HARDWARE LAYER                               │  │
│  │  ┌────────────┬──────────────┬─────────────┬───────────┐ │  │
│  │  │ IR Touch   │ Projector    │  USB Mic    │   Pi Cam  │ │  │
│  │  │ Frame      │ (HDMI+Relay) │  (ALSA)     │  (v2/v3)  │ │  │
│  │  └────────────┴──────────────┴─────────────┴───────────┘ │  │
│  │         Raspberry Pi 4/5 (4GB+ RAM)                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

External Services:
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Nextcloud  │    │  Firebase   │    │ OpenAI API  │
│   Storage   │◄───┤    Auth     │◄───┤   (GPT-4)   │
└─────────────┘    └─────────────┘    └─────────────┘
```

---

## 📁 Complete Folder Structure

```
NovaBoard/
├── frontend/                    # React UI (Existing)
│   ├── src/
│   ├── public/
│   └── package.json
│
├── backend/                     # NEW: Python Engine
│   ├── nova_engine/
│   │   ├── __init__.py
│   │   ├── api/                 # Flask REST API
│   │   │   ├── __init__.py
│   │   │   ├── app.py
│   │   │   ├── routes/
│   │   │   │   ├── canvas.py
│   │   │   │   ├── media.py
│   │   │   │   ├── recording.py
│   │   │   │   ├── ai.py
│   │   │   │   └── sync.py
│   │   │   └── middleware/
│   │   │       └── auth.py
│   │   │
│   │   ├── engines/
│   │   │   ├── canvas_engine.py
│   │   │   ├── media_processor.py
│   │   │   ├── recording_engine.py
│   │   │   └── ai_pipeline.py
│   │   │
│   │   ├── sync/
│   │   │   ├── sync_scheduler.py
│   │   │   ├── nextcloud_adapter.py
│   │   │   ├── firebase_adapter.py
│   │   │   └── queue_manager.py
│   │   │
│   │   ├── hardware/
│   │   │   ├── gpio_controller.py
│   │   │   ├── touch_handler.py
│   │   │   ├── projector_control.py
│   │   │   └── camera_controller.py
│   │   │
│   │   ├── ai/
│   │   │   ├── whisper_engine.py    # Offline STT
│   │   │   ├── ocr_engine.py        # Tesseract
│   │   │   ├── cloud_ai.py          # GPT API
│   │   │   └── models/              # Local AI models
│   │   │       ├── whisper-small/
│   │   │       └── tesseract/
│   │   │
│   │   ├── storage/
│   │   │   ├── db.py                # SQLite ORM
│   │   │   ├── file_manager.py
│   │   │   └── cache.py
│   │   │
│   │   └── utils/
│   │       ├── logger.py
│   │       ├── config.py
│   │       └── helpers.py
│   │
│   ├── requirements.txt
│   └── setup.py
│
├── electron/                   # NEW: Electron Wrapper
│   ├── main.js                 # Electron main process
│   ├── preload.js
│   ├── package.json
│   └── renderer/               # Points to frontend build
│
├── services/                   # NEW: System Services
│   ├── nova-backend.service    # Systemd service for Flask
│   ├── nova-electron.service   # Systemd service for Electron
│   ├── nova-sync.service       # Background sync daemon
│   └── nova-boot.sh            # Boot script
│
├── config/                     # NEW: Configuration
│   ├── nova.conf               # Main config
│   ├── hardware.json           # Hardware mappings
│   ├── network.json            # Network settings
│   └── ai.json                 # AI model configs
│
├── scripts/                    # NEW: Deployment Scripts
│   ├── install.sh              # Full installation
│   ├── update.sh               # Auto-update script
│   ├── setup-pi.sh             # Raspberry Pi setup
│   └── build-release.sh        # Build for deployment
│
├── docs/                       # Enhanced Documentation
│   ├── ARCHITECTURE.md
│   ├── API_SPEC.md
│   ├── DEPLOYMENT.md
│   ├── HARDWARE_GUIDE.md
│   └── USER_MANUAL.md
│
└── tests/                      # NEW: Test Suite
    ├── unit/
    ├── integration/
    └── e2e/
```

---

## 🔧 Core Modules Specification

### 1. **Canvas Engine** (`backend/nova_engine/engines/canvas_engine.py`)
- Manages infinite canvas state
- Handles IR touch events
- Pen/highlighter/shapes rendering
- Export to PNG/PDF
- Undo/Redo stack

### 2. **Recording Engine** (`backend/nova_engine/engines/recording_engine.py`)
- Screen capture using `python-mss` or `pyautogui`
- Audio capture using `pyaudio` (ALSA)
- Encoding using FFmpeg
- Optional teacher video bubble (Pi Camera)
- Auto-naming and compression
- Enqueue for sync

### 3. **AI Pipeline** (`backend/nova_engine/ai/`)
- **Offline**: Whisper-small for STT, Tesseract for OCR
- **Online**: GPT-4 for summarization, quiz generation
- Auto-transcript generation
- Note extraction from handwriting

### 4. **Sync Scheduler** (`backend/nova_engine/sync/`)
- Offline queue (SQLite)
- Retry logic on network restore
- Nextcloud WebDAV / Firebase Storage
- File versioning and conflict resolution

### 5. **Hardware Controller** (`backend/nova_engine/hardware/`)
- GPIO relay control for projector
- IR touch frame driver integration
- USB mic configuration
- Pi Camera control

---

## 🚀 Deployment Architecture

```
ClassNovaOS Boot Sequence:
1. Linux Lite boots
2. nova-backend.service starts (Flask API on :5000)
3. nova-sync.service starts (Background sync daemon)
4. nova-electron.service starts (Electron kiosk mode)
   ├─> Loads React frontend from :3000
   └─> Communicates with backend via :5000
```

---

## 📡 API Specification

### Canvas API
- `POST /api/canvas/stroke` - Add stroke
- `GET /api/canvas/:id` - Get canvas state
- `POST /api/canvas/export` - Export as PNG/PDF

### Recording API
- `POST /api/recording/start` - Start recording
- `POST /api/recording/stop` - Stop and save
- `GET /api/recording/:id` - Get recording metadata

### AI API
- `POST /api/ai/transcribe` - Transcribe audio
- `POST /api/ai/ocr` - Extract text from image
- `POST /api/ai/summarize` - Generate lesson summary

### Sync API
- `POST /api/sync/trigger` - Manual sync
- `GET /api/sync/status` - Get sync queue status

---

## 🎨 UI Integration

The **existing React frontend** will be wrapped in **Electron** for kiosk mode:
- Fullscreen on boot
- No browser chrome
- Touch-optimized
- IPC communication with backend

---

## 📦 Next Steps

I will now generate:
1. Backend Python engine (Flask API)
2. Electron wrapper
3. System services
4. Installation scripts
5. Hardware integration layer

Would you like me to proceed with generating all the code modules?
