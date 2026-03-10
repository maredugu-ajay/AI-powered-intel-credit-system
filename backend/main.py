"""
IntelCredit - AI-Powered Corporate Credit Appraisal Engine
Main FastAPI Application

This is the entry point for the backend server.
Run with: uvicorn main:app --reload --port 8000
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

import config
from routers import documents, analysis, research, cam

# Create FastAPI app
app = FastAPI(
    title=config.APP_NAME,
    description=config.APP_DESCRIPTION,
    version=config.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(documents.router)
app.include_router(analysis.router)
app.include_router(research.router)
app.include_router(cam.router)

# Serve React production build if available
frontend_dist = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

if os.path.exists(frontend_dist):
    # Production: serve built React app
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")


@app.get("/")
async def root():
    """Serve the frontend or show API info."""
    dist_index = os.path.join(frontend_dist, "index.html")
    if os.path.exists(dist_index):
        return FileResponse(dist_index)
    return {
        "app": config.APP_NAME,
        "version": config.APP_VERSION,
        "description": config.APP_DESCRIPTION,
        "docs": "/docs",
        "frontend": "Run 'cd frontend && npm run dev' for React dev server on port 3000",
        "endpoints": {
            "documents": "/api/documents",
            "analysis": "/api/analysis",
            "research": "/api/research",
            "cam": "/api/cam",
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "app": config.APP_NAME, "version": config.APP_VERSION}


@app.get("/api")
async def api_info():
    return {
        "app": config.APP_NAME,
        "version": config.APP_VERSION,
        "endpoints": {
            "POST /api/documents/upload": "Upload and parse a document",
            "POST /api/analysis/ratios": "Compute financial ratios",
            "POST /api/analysis/gst": "Analyze GST returns",
            "POST /api/analysis/banking": "Analyze bank statements",
            "POST /api/analysis/full": "Full financial analysis",
            "POST /api/research/secondary": "Conduct secondary research",
            "POST /api/research/insights": "Add primary insight",
            "POST /api/cam/generate": "Generate full CAM report",
        }
    }


# SPA catch-all MUST be registered last so it doesn't intercept API routes
if os.path.exists(frontend_dist):
    @app.get("/{full_path:path}")
    async def serve_react(full_path: str):
        """Serve React SPA - all non-API routes go to index.html."""
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=config.HOST, port=config.PORT, reload=config.DEBUG)
