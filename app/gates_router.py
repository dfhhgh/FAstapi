from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse

from app.supabase_client import get_supabase

gates_router = APIRouter()


@gates_router.get(
    "/public/info",
    summary="Public information",
    description="Returns a public message. No authentication required.",
)
async def public_info():
    return {"message": "Welcome stranger! This info is public."}


@gates_router.get(
    "/protected/profile",
    summary="Protected profile",
    description="Returns verified user profile. Requires a valid Bearer token.",
)
async def protected_profile(authorization: str | None = Header(None)):
    if not authorization:
        return JSONResponse(status_code=401, content={"error": "Access token required"})

    parts = authorization.split(" ", 1)
    if len(parts) != 2 or parts[0] != "Bearer" or not parts[1].strip():
        return JSONResponse(status_code=401, content={"error": "Access token required"})

    token = parts[1].strip()

    try:
        client = get_supabase()
        result = client.auth.get_user(token)
    except Exception:
        return JSONResponse(status_code=401, content={"error": "Invalid or expired token"})

    if result.user is None:
        return JSONResponse(status_code=401, content={"error": "Invalid or expired token"})

    user = result.user

    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at,
    }
