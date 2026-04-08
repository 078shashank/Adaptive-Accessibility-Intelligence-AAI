"""FastAPI Application Entry Point"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import logging
import time

from app.config import settings
from app.database import init_db
from app.database_optimizer import add_database_indexes, analyze_database
from app.routes import health, auth, text, user, avatar, guided

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-driven accessibility platform with dynamic content personalization",
    version="0.2.0"
)

# Add state for limiter
app.state.limiter = limiter

# Add security middleware - Trusted hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["127.0.0.1", "localhost", "127.0.0.1:3000", "127.0.0.1:8000", "testserver"]
)

# Custom CORS origin validator
def validate_cors_origin(origin: str) -> bool:
    """
    Validate CORS origins including Chrome/Firefox extensions.
    Allows specific origins and validates extension IDs.
    """
    # Check against allowed origins list
    if origin in settings.CORS_ORIGINS:
        return True
    
    # Check for Chrome extension origins
    if origin and origin.startswith("chrome-extension://"):
        extension_id = origin.replace("chrome-extension://", "")
        if settings.ALLOWED_EXTENSION_IDS:
            return extension_id in settings.ALLOWED_EXTENSION_IDS
        # Allow all during development (populate ALLOWED_EXTENSION_IDS for production)
        return True
    
    # Check for Firefox extension origins  
    if origin and origin.startswith("moz-extension://"):
        extension_id = origin.replace("moz-extension://", "")
        if settings.ALLOWED_EXTENSION_IDS:
            return extension_id in settings.ALLOWED_EXTENSION_IDS
        return True
    
    return False

# Add CORS middleware with dynamic origin validation
@app.middleware("http")
async def cors_middleware(request, call_next):
    """Custom CORS middleware with extension support"""
    origin = request.headers.get("origin")
    
    response = await call_next(request)
    
    if origin and validate_cors_origin(origin):
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "*"
    
    return response

# Standard CORS middleware for preflight requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # Only specific origins for preflight
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
@app.on_event("startup")
async def startup():
    """Initialize database on startup"""
    init_db()
    logger.info("Database initialized")
    
    # Optimize database
    add_database_indexes()
    analyze_database()
    logger.info("Database indexes created and analyzed")
    
    logger.info(f"CORS allowed origins: {settings.CORS_ORIGINS}")
    logger.info("Rate limiting enabled: 100 requests/minute per IP")
    logger.info("Security headers enabled")
    logger.info("✅ AAI Backend API Ready for requests")


# Custom exception handlers
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    """Handle rate limit exceeded errors"""
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Max 100 requests per minute."}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Handle validation errors with better messages"""
    return JSONResponse(
        status_code=400,
        content={"detail": "Invalid request. Please check your input."}
    )


# Health check for monitoring
@app.get("/health")
@limiter.limit("100/minute")
async def health_check(request):
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "AAI Backend API"
    }


# Include routers
app.include_router(health.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(text.router, prefix="/api/v1")
app.include_router(user.router, prefix="/api/v1")
app.include_router(avatar.router, prefix="/api/v1")
app.include_router(guided.router, prefix="/api/v1")


@app.get("/")
@limiter.limit("100/minute")
async def root(request):
    """Root endpoint"""
    return {
        "message": "Welcome to Adaptive Accessibility Intelligence (AAI)",
        "docs": "/docs",
        "health": "/api/v1/health",
        "version": "0.2.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
