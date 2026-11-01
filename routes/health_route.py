"""
Health check API route.

Defines a simple endpoint to verify that the service is up and running.
Returns a JSON response with a "status" key set to "ok".
"""

from fastapi import APIRouter, Request

api_router = APIRouter()


@api_router.get("/health", tags=["Health"])
async def health_check():
    """
    Simple health check endpoint.
    Returns a JSON response with a single key "status" and value "ok".
    """
    return {"status": "ok"}


@api_router.get("/health/version", tags=["Health"])
async def health_version(request: Request) -> dict[str, str]:
    """Return the configured application version."""
    return {"version": request.app.version}
