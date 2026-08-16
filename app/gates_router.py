from fastapi import APIRouter, Header, HTTPException

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
    description="Returns profile data. Requires a valid Bearer token.",
)
async def protected_profile(authorization: str | None = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail={"error": "Access token required"})

    parts = authorization.split(" ", 1)
    if len(parts) != 2 or parts[0] != "Bearer" or not parts[1].strip():
        raise HTTPException(status_code=401, detail={"error": "Access token required"})

    return {"message": "Profile data", "token_received": True}
