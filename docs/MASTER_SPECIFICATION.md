# NOVA BOARD — FULL-FLEDGED MASTER SOFTWARE SPECIFICATION

## 1. Executive Summary
**NovaBoard** is a comprehensive, software-only Smart Classroom platform designed to transform any standard projection setup into a fully digital, AI-powered, collaborative teaching environment. It eliminates the need for expensive interactive hardware by leveraging modern web technologies to turn any computer and projector into a smart whiteboard.

**Users**:
*   **Teachers**: Deliver engaging, multimedia-rich lessons with AI assistance.
*   **Students**: Join sessions via personal devices for real-time viewing, interaction, and note-taking.
*   **Admins**: Manage schools, users, and content at scale.

**Value Proposition**: NovaBoard democratizes smart education. It provides the advanced features of a $5,000 smartboard—interactive whiteboarding, session recording, AI transcription, and real-time collaboration—using only software. It is offline-first, low-bandwidth friendly, and designed for the reality of diverse classroom infrastructures.

## 2. Complete Feature System

### A. Teaching Tools
*   **Interactive Whiteboard**: Infinite canvas, multi-page support, vector-based rendering (Zoom/Pan).
*   **Tools**: Pen (pressure-sensitive), Highlighter, Eraser, Shapes, Text, Sticky Notes, Laser Pointer.
*   **Media Support**: Drag-and-drop import for Images, Videos, PDFs, and PPTs (converted to images).
*   **Presentation Mode**: Slide navigation, laser pointer, blackout screen.
*   **Export**: High-fidelity PDF and PNG export of the entire board or specific regions.

### B. AI Features
*   **Live Subtitles**: Real-time speech-to-text (Whisper) displayed as captions.
*   **Smart Summaries**: Auto-generated lesson summaries with key points and action items (LLM).
*   **AI Tutor**: "Explain this" context menu for math/code/science concepts on the board.
*   **OCR**: Convert handwritten text or text inside images into editable digital text.
*   **Engagement Analytics**: AI analysis of student participation and attention.

### C. Student Interaction
*   **Join Flow**: Simple 6-digit code or QR code join.
*   **Live View**: Real-time mirroring of the teacher's canvas on student devices.
*   **Interaction**: "Raise Hand", "Slow Down/Speed Up" reactions, Polls, and Quizzes.
*   **Collaboration**: Teacher-controlled "Student Mode" allowing students to draw on the board.

### D. Classroom Management
*   **Session Management**: Create, schedule, and archive classes.
*   **LMS Integration**: Sync rosters and assignments with Google Classroom, Moodle, and Canvas.
*   **Attendance**: Auto-attendance based on session join time.

### E. File System & Storage
*   **Cloud Drive**: Personal storage for every teacher.
*   **Versioning**: Automatic version history for all boards.
*   **Asset Library**: Shared folder for 3D models, templates, and reusable assets.

### F. Admin & Multi-School
*   **Multi-Tenancy**: Support for multiple schools/districts under one deployment.
*   **RBAC**: Granular permissions for Admins, Teachers, and Students.
*   **Audit Logs**: Full tracking of user actions and data access.

### G. Offline-First
*   **Local-First Architecture**: App works fully offline using IndexedDB.
*   **Background Sync**: Changes sync to cloud automatically when connection is restored.
*   **Conflict Resolution**: CRDT-based merging to handle concurrent offline edits.

## 3. High-Level Architecture

```mermaid
graph TD
    subgraph Client_Layer
        Web_App[React PWA]
        Mobile_App[React Native]
    end

    subgraph Edge_Layer
        CDN[Cloudflare CDN]
        LB[Load Balancer]
        API_GW[API Gateway / GraphQL]
    end

    subgraph Service_Layer
        Auth_Svc[Auth Service]
        Board_Svc[Whiteboard Service]
        Collab_Svc[Real-time Collab (WebSocket)]
        Media_Svc[Media Pipeline]
        AI_Svc[AI Orchestrator]
        Analytics_Svc[Analytics Engine]
    end

    subgraph Data_Layer
        DB[(PostgreSQL)]
        Cache[(Redis)]
        Obj_Store[(S3 / MinIO)]
        Vector_DB[(Vector DB for AI)]
    end

    subgraph AI_Workers
        Whisper[Whisper Worker]
        LLM[LLM Worker]
        OCR[OCR Worker]
    end

    Web_App --> LB
    LB --> API_GW
    API_GW --> Auth_Svc
    API_GW --> Board_Svc
    API_GW --> Media_Svc
    
    Web_App -- WebSocket --> Collab_Svc
    Collab_Svc --> Cache
    
    Media_Svc --> Obj_Store
    Media_Svc --> AI_Svc
    AI_Svc --> Whisper
    AI_Svc --> LLM
```

## 4. Tech Stack

### Frontend
*   **Framework**: React 19 + TypeScript + Vite.
*   **State Management**: Jotai (Atomic state) + Yjs (CRDTs).
*   **Canvas Engine**: Custom engine based on HTML5 Canvas / WebGL (or Excalidraw core).
*   **Styling**: Tailwind CSS + CSS Modules.

### Backend
*   **API**: Node.js (NestJS) or Go (Fiber).
*   **Real-time**: Hocuspocus (Yjs WebSocket Server) or Socket.IO.
*   **Database**: PostgreSQL (Prisma ORM).
*   **Cache**: Redis.
*   **Queue**: BullMQ (Redis-based) or RabbitMQ.

### AI & Media
*   **Transcription**: OpenAI Whisper (Self-hosted or API).
*   **LLM**: Llama 3 (Self-hosted) or OpenAI GPT-4o.
*   **Media Processing**: FFmpeg (WASM for client-side, Server-side for heavy lifting).

## 5. Real-Time Collaboration Engine
*   **Protocol**: Yjs (CRDT) over WebSocket.
*   **Data Structure**: `Y.Map` for scene state, `Y.Array` for elements.
*   **Conflict Resolution**: Mathematical guarantee of eventual consistency via CRDTs.
*   **Awareness**: Ephemeral state (cursors, selection) broadcast via WebSocket, not stored in DB.

## 6. Media Recording Pipeline
1.  **Capture**: `navigator.mediaDevices.getDisplayMedia` (Screen) + `getUserMedia` (Mic).
2.  **Composition**: Canvas stream + Audio track merged in browser.
3.  **Encoding**: `MediaRecorder` API (WebM/VP9).
4.  **Upload**: Chunked upload to S3 (Multipart upload).
5.  **Processing**: Server triggers FFmpeg job -> Convert to MP4 (H.264) -> Extract Audio -> Send to Whisper.

## 7. AI Pipeline
1.  **Ingest**: Audio extracted from recording.
2.  **Transcribe**: Whisper generates timestamped SRT/VTT.
3.  **Analyze**: Transcript fed to LLM for summarization and key-point extraction.
4.  **Index**: Vector embeddings stored in Vector DB for semantic search ("Show me where the teacher talked about photosynthesis").

## 8. Data Models (Simplified)

### User
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR UNIQUE,
  role ENUM('TEACHER', 'STUDENT', 'ADMIN'),
  school_id UUID
);
```

### Session
```sql
CREATE TABLE sessions (
  id UUID PRIMARY KEY,
  teacher_id UUID,
  title VARCHAR,
  start_time TIMESTAMP,
  end_time TIMESTAMP,
  recording_url VARCHAR,
  transcript_text TEXT
);
```

### Board State
*   Stored as a JSON blob in Object Storage (snapshots) + CRDT update logs in DB.

## 9. UI/UX System
*   **Theme**: "NovaBoard Orange" (Primary: #e8590c, Dark: #000000).
*   **Layouts**:
    *   **Dashboard**: Grid view of classes, Recent Sessions list, Analytics summary.
    *   **Whiteboard**: Minimalist toolbar (left), Infinite canvas (center), Collab/Chat (right drawer).
    *   **Student View**: Read-only canvas, "Raise Hand" FAB, Reaction bar.

## 10. API Specification (Key Endpoints)
*   `POST /auth/login`: Authenticate user.
*   `POST /sessions`: Start a new class session.
*   `GET /sessions/:id/join`: Get join token for students.
*   `POST /media/upload`: Upload recording chunk.
*   `GET /ai/summary/:sessionId`: Get AI-generated summary.

## 11. Security & Privacy
*   **Auth**: OAuth2 (Google/Microsoft) + JWT Access/Refresh tokens.
*   **Data**: AES-256 encryption at rest (DB & S3). TLS 1.3 in transit.
*   **Privacy**: "Recording Consent" modal for all participants. GDPR "Right to be Forgotten" implementation.

## 12. Offline & Sync
*   **Storage**: IndexedDB (Dexie.js) stores all board state and assets locally.
*   **Sync**: Service Worker intercepts requests. Background Sync API pushes changes when online.
*   **UX**: "Offline" badge in UI. "Syncing..." spinner when reconnecting.

## 13. DevOps
*   **Container**: Dockerfile for every service.
*   **Orchestration**: Kubernetes (K8s) or AWS ECS.
*   **CI/CD**: GitHub Actions -> Build -> Test -> Deploy to Staging/Prod.

## 14. Analytics
*   **Metrics**: Daily Active Users (DAU), Session Length, Tool Usage, Student Engagement Score.
*   **Pipeline**: Clickhouse or BigQuery for high-volume event ingestion.

## 15. Roadmap
*   **Phase 1 (MVP)**: Whiteboard, Local Recording, Basic Join.
*   **Phase 2**: Cloud Sync, AI Transcription, LMS Integration.
*   **Phase 3**: Mobile Apps, Advanced AI (Tutor), Enterprise Features.
