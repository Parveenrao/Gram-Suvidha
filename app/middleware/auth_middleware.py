from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError, jwt
from app.config import settings
import time
import logging

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────
# PUBLIC ROUTES — no token needed
# ─────────────────────────────────────────
PUBLIC_ROUTES = [
    "/",
    "/docs",
    "/openapi.json",
    "/redoc",
    "/api/auth/login",
    "/api/auth/register",
    "/api/villages/",
    "/api/announcements/",
    "/api/projects/",
    "/api/budget/",
    "/api/documents/",
]

def is_public_route(path: str) -> bool:
    """Check if route is public — no auth needed."""
    for route in PUBLIC_ROUTES:
        if path.startswith(route):
            return True
    return False


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        logger.info(f"{request.method} {request.url.path}")

        try:
            response = await call_next(request)

            process_time = round((time.time() - start_time) * 1000, 2)
            response.headers["X-Process-Time"] = f"{process_time}ms"

            return response

        except Exception as e:
            logger.exception(e)
            raise



class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that logs:
    - Who is making the request (user id from token if available)
    - What endpoint they hit
    - What status code was returned
    """

    async def dispatch(self, request: Request, call_next):

        # Try to get user from token for logging
        user_id = "anonymous"
        token = request.headers.get("Authorization")
        if token and token.startswith("Bearer "):
            try:
                payload = jwt.decode(
                    token.split(" ")[1],
                    settings.SECRET_KEY,
                    algorithms=[settings.ALGORITHM]
                )
                user_id = f"user_{payload.get('sub')}"
            except JWTError:
                user_id = "invalid_token"

        # Log request details
        logger.info(
            f"REQUEST | "
            f"User: {user_id} | "
            f"Method: {request.method} | "
            f"Path: {request.url.path}"
        )

        response = await call_next(request)

        # Log response
        logger.info(
            f"RESPONSE | "
            f"User: {user_id} | "
            f"Path: {request.url.path} | "
            f"Status: {response.status_code}"
        )

        return response