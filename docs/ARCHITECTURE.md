# NovaBoard Software Architecture Specification

## Executive Summary
NovaBoard is a comprehensive, software-only Smart Classroom solution that transforms any standard projection setup into an interactive, AI-powered teaching environment. It unifies interactive whiteboarding, session recording, real-time transcription, and classroom analytics into a single, offline-first platform, empowering teachers to deliver engaging lessons without specialized hardware.

## 1. Product Scope & Feature List

### Interactive Whiteboard
*   **Infinite Canvas**: Zoomable, pannable multi-page workspace.
*   **Tools**: Pen, highlighter, eraser, shapes, text, sticky notes.
*   **Media**: Image import, PDF/PPT slide import (converted to images).
*   **Collaboration**: Real-time multi-user editing with cursor presence.
*   **History**: Robust undo/redo stack, version history.

### Recording & Playback
*   **Session Recording**: Captures whiteboard canvas + audio (via microphone).
*   **Smart Playback**: Timeline with chapter markers based on slide changes.
*   **Export**: MP4 video download, PDF export of notes.

### Smart Notes & AI
*   **Live Transcription**: Real-time speech-to-text displayed as captions.
*   **AI Summarization**: Post-session summary generation (bullet points, key terms).
*   **OCR**: Text extraction from uploaded images/slides.
*   **AI Tutor**: "Explain this" feature for selected board content.

### Classroom Management
*   **Join Flow**: QR code / PIN join for students.
*   **Roles**: Teacher (host), Student (view/interact), Admin.
*   **File Cabinet**: Local/Cloud storage for lesson plans and assets.

### Offline-First
*   **Local Caching**: Full functionality without internet; syncs when online.
*   **PWA**: Installable on any device (Windows, Mac, ChromeOS, iPad, Android).

## 2. High-Level Architecture

### Components
1.  **Client (Frontend)**: React + TypeScript PWA. Handles whiteboard logic, rendering (Canvas/WebGL), media capture, and local state.
2.  **API Gateway**: Entry point for all client requests. Routes to microservices.
3.  **Auth Service**: Manages users, sessions, and roles (OAuth2/JWT).
4.  **Signaling Service**: WebSocket server for real-time board synchronization.
5.  **Media Service**: Handles upload/storage of recordings and assets.
6.  **AI Worker Pipeline**: Async jobs for transcription (Whisper), summarization (LLM), and OCR.
7.  **Data Store**:
    *   **PostgreSQL**: Relational data (users, classes, metadata).
    *   **Redis**: Hot state (presence, session cache).
    *   **S3/MinIO**: Object storage (images, videos, PDFs).

### Data Flow (Single Session)
1.  **Start**: Teacher initializes session (Client -> API -> DB).
2.  **Interact**: Draw events sent via WebSocket (Client -> Signaling -> Clients).
3.  **Record**: Audio/Canvas stream captured locally, chunked, uploaded (Client -> Media Service -> S3).
4.  **Process**: Job enqueued (Media Service -> Queue -> AI Worker).
5.  **Result**: Transcript/Summary stored (AI Worker -> DB) and pushed to client.

## 3. Tech Stack Recommendation

*   **Frontend**: React 19, TypeScript, Vite, Jotai (state), React Router.
*   **Real-time**: Socket.IO or Hocuspocus (Yjs) for CRDT-based sync.
*   **Backend**: Node.js (NestJS) or Go (Fiber).
*   **Database**: PostgreSQL (Supabase for rapid dev), Redis.
*   **Storage**: AWS S3 or MinIO (self-hosted).
*   **AI/ML**: OpenAI API (MVP) -> Self-hosted Whisper/Llama (Scale).
*   **DevOps**: Docker, GitHub Actions, Vercel (Frontend), Railway/AWS (Backend).

## 4. Realtime Collaboration Protocol

We will use **CRDTs (Conflict-free Replicated Data Types)** via **Yjs** for board state.
*   **Why**: Ensures consistency without central locking, perfect for offline-first (merges changes when back online).
*   **Transport**: WebSocket provider for live sync; IndexedDB provider for offline persistence.

## 5. Data Models (Core Schema)

### Session
```json
{
  "id": "uuid",
  "teacherId": "uuid",
  "title": "Math 101 - Calculus",
  "startTime": "timestamp",
  "endTime": "timestamp",
  "recordingUrl": "url",
  "transcriptId": "uuid"
}
```

### BoardElement
```json
{
  "id": "uuid",
  "type": "rectangle | text | freedraw",
  "x": 100,
  "y": 200,
  "properties": { "stroke": "#000", "fill": "transparent" },
  "version": 1
}
```

## 6. Security & Privacy
*   **Encryption**: TLS 1.3 for transit, AES-256 for storage.
*   **Auth**: RBAC (Role-Based Access Control).
*   **Compliance**: GDPR compliant (data export/delete), FERPA aligned (student data privacy).

## 7. Roadmap & Milestones

### Phase 1: MVP (Weeks 1-6)
*   [x] Core Whiteboard (NovaBoard Rebrand).
*   [ ] Offline PWA support.
*   [ ] Basic Recording (Local download).
*   [ ] Student Join (Read-only view).

### Phase 2: Beta (Weeks 7-12)
*   [ ] Cloud Sync & Auth.
*   [ ] Real-time Collaboration.
*   [ ] AI Transcription (Cloud API).

### Phase 3: Scale (Months 4-6)
*   [ ] LMS Integration.
*   [ ] Advanced Analytics.
*   [ ] Self-hosted AI models.
