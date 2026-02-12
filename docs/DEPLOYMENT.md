# Deployment Guide - Vercel

## Quick Deploy to Vercel

### 1. Install Vercel CLI
```bash
npm install -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Deploy Frontend (Next.js)
```bash
cd /root/.openclaw/workspace/creator-analytics-saas
cd frontend
vercel deploy --prod
```

### 4. Set Environment Variables
In Vercel Dashboard:
```
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

---

## Deploy Backend Separately

### Option A: Railway.app (Recommended)

1. Go to [Railway.app](https://railway.app)
2. Connect GitHub repo
3. Set environment variables in Railway dashboard:
   ```
   DATABASE_URL=postgresql://...
   REDIS_URL=redis://...
   SECRET_KEY=your-secret-key
   ```
4. Deploy

### Option B: Render.com (Recommended for Backend)

#### Method 1: Blueprint Deploy (Fastest)

1. Go to [Render.com](https://render.com)
2. Sign up/Login with GitHub
3. Go to [Blueprints](https://dashboard.render.com/blueprints)
4. Click "New Blueprint Instance"
5. Connect your GitHub repository
6. Select file: `backend/render.yaml`
7. Click "Apply"

Render will create:
- Web Service (Backend API)
- PostgreSQL Database
- All environment variables

#### Method 2: Manual Deploy

1. **Create Web Service**
   - Dashboard → "New +" → "Web Service"
   - Connect GitHub repo
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

2. **Create PostgreSQL Database**
   - Dashboard → "New +" → "PostgreSQL"
   - Name: `creator-analytics-db`
   - Plan: Free (for dev) or $7/mo (production)

3. **Set Environment Variables**
   ```
   SECRET_KEY= (Render can generate random)
   CORS_ORIGINS=["http://localhost:3000", "https://*.vercel.app"]
   
   # Platform API Keys (get from developer portals)
   YOUTUBE_API_KEY=...
   TIKTOK_API_KEY=...
   INSTAGRAM_ACCESS_TOKEN=...
   TWITTER_API_KEY=...
   OPENAI_API_KEY=...
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for build

### Option C: AWS/GCP

```bash
# Using Docker
cd backend
docker build -t creator-analytics-backend .
docker run -p 8000:8000 creator-analytics-backend
```

---

## Environment Variables Needed

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@host:5432/db
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-super-secret-key
YOUTUBE_API_KEY=your-youtube-key
TIKTOK_API_KEY=your-tiktok-key
INSTAGRAM_ACCESS_TOKEN=your-ig-token
TWITTER_API_KEY=your-twitter-key
OPENAI_API_KEY=your-openai-key
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Architecture After Deploy

```
┌─────────────────────────────────────────┐
│         Vercel (Frontend)                │
│  https://creator-analytics.vercel.app   │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│    Railway/Render/AWS (Backend API)     │
│  https://api.creator-analytics.com      │
│  ├── FastAPI                            │
│  ├── PostgreSQL                          │
│  ├── Redis                              │
│  └── ML Prediction Engine                │
└─────────────────────────────────────────┘
```

---

## Domain Setup (Optional)

### Vercel Domain
- Frontend: `creator-analytics.vercel.app` (auto)
- Custom: `app.creatoranalytics.com` → Vercel DNS

### Backend Domain  
- Custom: `api.creatoranalytics.com` → Backend IP

---

## CI/CD Setup

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
          vercel-args: '--prod'
```

---

## Status Commands

```bash
# Check deployment status
vercel list

# View logs
vercel logs --prod

# Rollback
vercel rollback
```
