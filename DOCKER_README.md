# NovaBoard Docker Deployment Guide

## Prerequisites

1. **Docker Desktop** installed and running
2. **Git** (for cloning the repository)
3. At least **4GB RAM** available for Docker

## Quick Start

```bash
# Clone the repository (if needed)
git clone <repository-url>
cd NovaBoard

# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up --build -d
```

Access the application at: **http://localhost:3000**

## Docker Services

### Backend (Port 5001, 5002)
- Python Flask API
- Recording daemon
- 3D model management
- File storage

### Frontend (Port 3000)
- Excalidraw UI
- Built with Vite
- Served by Nginx
- Proxies API requests to backend

## File Structure

```
NovaBoard/
├── docker-compose.yml          # Orchestration config
├── .dockerignore               # Excluded files
├── backend/
│   ├── Dockerfile             # Backend container
│   ├── requirements.txt       # Python dependencies
│   └── data/                  # Persisted data (volume)
└── excalidraw-app/
    ├── Dockerfile             # Frontend container
    ├── nginx.conf             # Nginx configuration
    └── .env.production        # Production env vars
```

## Troubleshooting

### Docker Credential Error

If you see: `error getting credentials - err: exec: "docker-credential-desktop": executable file not found`

**Solution:**
1. Open Docker Desktop preferences
2. Uncheck "Securely store Docker logins in macOS keychain"
3. Restart Docker Desktop
4. Try building again

OR manually fix the Docker config:

```bash
# Edit Docker config
nano ~/.docker/config.json

# Change "credsStore": "desktop" to "credsStore": "osxkeychain"
# Or remove the "credsStore" line entirely
```

### Build Fails

```bash
# Clean build cache
docker-compose down -v
docker system prune -a

# Rebuild
docker-compose build --no-cache
```

### Port Already in Use

```bash
# Check what's using the port
lsof -i :3000
lsof -i :5001

# Kill the process
kill -9 <PID>
```

### Frontend Not Loading

1. Check backend is running: `curl http://localhost:5001/`
2. Check frontend logs: `docker-compose logs frontend`
3. Verify nginx config: `docker exec novaboard-frontend nginx -t`

## Data Persistence

Data is persisted in host directories:
- `./backend/data` - Media files, 3D models
- `./backend/instance` - SQLite database

To backup:
```bash
tar -czf novaboard-backup.tar.gz backend/data backend/instance
```

## Development vs Production

### Development (Current Setup)
- Hot reload disabled
- Production builds
- Nginx serves static files
- SQLite database

### For True Production
1. Use PostgreSQL instead of SQLite
2. Add SSL/TLS certificates
3. Configure environment-specific secrets
4. Set up proper logging
5. Use Docker volumes instead of bind mounts

## Useful Commands

```bash
# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Build specific service
docker-compose build backend
docker-compose build frontend

# Enter container shell
docker exec -it novaboard-backend /bin/bash
docker exec -it novaboard-frontend /bin/sh

# Check service health
docker-compose ps
```

## Environment Variables

### Frontend (.env.production)
```
VITE_APP_BACKEND_V2_POST_URL=http://backend:5001/api/v2/post/
VITE_APP_BACKEND_V2_GET_URL=http://backend:5001/api/v2/
VITE_APP_COLLABORATION_SERVER=http://backend:5001
```

### Backend (docker-compose.yml)
```
FLASK_ENV=production
SECRET_KEY=<change-this-in-production>
PYTHONUNBUFFERED=1
```

## Performance Tuning

### Allocate More Resources
In Docker Desktop:
- Settings → Resources
- Increase CPUs to 4
- Increase Memory to 8GB

### Optimize Build Time
```bash
# Use BuildKit
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

docker-compose build
```

## Security Notes

⚠️ **Before deploying to production:**

1. Change `SECRET_KEY` in docker-compose.yml
2. Remove demo data
3. Add authentication
4. Enable HTTPS
5. Review CORS settings
6. Set up firewall rules

## Support

For issues:
1. Check logs: `docker-compose logs`
2. Verify Docker Desktop is running
3. Ensure ports 3000, 5001, 5002 are available
4. Try rebuilding: `docker-compose build --no-cache`
