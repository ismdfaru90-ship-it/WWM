# OpenHands Deployment Guide

This document describes how to deploy OpenHands with the frontend on Cloudflare Pages and the backend on Railway.

## Architecture

```
GitHub Repository
       │
       ▼
    Railway (Backend)
       │
       ▼
Cloudflare Pages (Frontend)
       │
       ▼
   User Browser
```

## Prerequisites

1. **GitHub Account** with access to your fork of OpenHands
2. **Railway Account** - Sign up at https://railway.app
3. **Cloudflare Account** - Sign up at https://cloudflare.com

## Setup Instructions

### Step 1: Fork the Repository

Fork the OpenHands repository to your GitHub account.

### Step 2: Configure Railway Backend

1. Create a new Railway project
2. Connect your GitHub repository to Railway
3. Set the following environment variables in Railway:

```bash
# Required
LLM_API_KEY=your_openrouter_api_key
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=openrouter/auto
PORT=3000
RUNTIME=docker

# Optional - For R2 storage
AWS_ACCESS_KEY_ID=your_r2_access_key
AWS_SECRET_ACCESS_KEY=your_r2_secret_key
AWS_S3_ENDPOINT_URL=https://your_account_id.r2.cloudflarestorage.com
```

### Step 3: Configure Cloudflare

1. Create a Cloudflare Pages project
2. Connect it to your GitHub repository
3. Set the build command: `cd frontend && npm install && npm run build`
4. Set the build output directory: `frontend/build`
5. Add the environment variable:
   - `VITE_BACKEND_BASE_URL` = Your Railway backend URL (e.g., `openhands-backend.up.railway.app`)

### Step 4: Configure GitHub Secrets

Add the following secrets to your GitHub repository (Settings → Secrets and variables → Actions):

| Secret Name | Description |
|------------|-------------|
| `RAILWAY_TOKEN` | Your Railway API token |
| `RAILWAY_PROJECT_ID` | Your Railway project ID |
| `LLM_API_KEY` | Your OpenRouter API key |
| `LLM_BASE_URL` | `https://openrouter.ai/api/v1` |
| `LLM_MODEL` | `openrouter/auto` |
| `CLOUDFLARE_API_TOKEN` | Cloudflare Pages API token |
| `CLOUDFLARE_ACCOUNT_ID` | Your Cloudflare account ID |
| `RAILWAY_BACKEND_URL` | Your Railway backend URL (for frontend) |

### Step 5: Deploy

Option A: Push to main branch - automatically triggers deployment
Option B: Go to Actions tab → Select "Deploy OpenHands" → Click "Run workflow"

## Environment Variables Reference

### Backend (Railway)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LLM_API_KEY` | Yes | - | OpenRouter API key |
| `LLM_BASE_URL` | Yes | `https://openrouter.ai/api/v1` | LLM provider base URL |
| `LLM_MODEL` | Yes | `openrouter/auto` | LLM model to use |
| `PORT` | Yes | `3000` | Server port |
| `RUNTIME` | Yes | `docker` | Runtime environment |
| `AWS_*` | No | - | R2 storage configuration |

### Frontend (Cloudflare Pages)

| Variable | Required | Description |
|----------|----------|-------------|
| `VITE_BACKEND_BASE_URL` | Yes | Backend URL (e.g., `openhands-backend.up.railway.app`) |
| `VITE_USE_TLS` | No | Set to `true` if using HTTPS |

## Troubleshooting

### Frontend can't connect to backend

1. Check that `VITE_BACKEND_BASE_URL` is correctly set
2. Verify the Railway backend is running
3. Check CORS settings in Railway

### Backend deployment fails

1. Verify all required environment variables are set
2. Check Railway logs for specific errors
3. Ensure Docker is available for the sandbox runtime

### LLM API errors

1. Verify `LLM_API_KEY` is correct
2. Check `LLM_BASE_URL` and `LLM_MODEL` are correct
3. Ensure your OpenRouter account has sufficient credits

## Monitoring

- **Railway**: Check deployment logs and metrics in Railway dashboard
- **Cloudflare Pages**: View deployment history and analytics in Cloudflare dashboard

## Security Notes

1. Never commit API keys to the repository
2. Use GitHub Secrets for all sensitive credentials
3. Consider using separate API keys for development and production
4. Enable CORS protection on Railway backend
