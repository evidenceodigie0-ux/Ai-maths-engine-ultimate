# AI Maths Engine Ultimate — deployable starter

This package contains a browser-based local polynomial maths interface and a FastAPI backend suitable for Render Docker deployment.

## Deploy
1. Upload all files in this folder to the root of a GitHub repository.
2. In Render, choose **New Web Service** and connect that repository.
3. Render detects the `Dockerfile`; create the service.
4. Once live, open the Render URL and check `/api/health` returns `{"status":"ok","service":"AI Maths Engine"}`.

## Notes
- `index.html` includes a local browser solver for its supported input types.
- Backend API endpoints: `GET /api/health`, `POST /api/solve` with JSON `{"question":"2*x+3=9"}`.
- This is a starter engine, not a system that solves every mathematics problem perfectly. For symbolic expressions use explicit multiplication, e.g. `2*x+3=9`.
