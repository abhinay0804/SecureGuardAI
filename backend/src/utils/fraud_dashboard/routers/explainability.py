import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/explainability", tags=["Explainability"])


class KeyPayload(BaseModel):
    provider: str
    api_key: str


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))

active_provider_file = os.path.join(project_root, ".active_explain_provider")
nvidia_key_file = os.path.join(project_root, ".nvidia_explain_key")
gemini_key_file = os.path.join(project_root, ".gemini_explain_key")


@router.get("/key")
def get_key():
    # Read active provider selection if stored
    active_provider = None
    if os.path.exists(active_provider_file):
        try:
            active_provider = open(active_provider_file, "r").read().strip().lower()
        except Exception:
            pass

    # Check key status for active provider or fallback order
    if active_provider == "gemini":
        has_gem = bool(os.getenv("GEMINI_API_KEY")) or os.path.exists(gemini_key_file)
        return {"provider": "gemini", "present": has_gem}
    elif active_provider == "nvidia":
        has_nv = bool(os.getenv("NVIDIA_API_KEY")) or os.path.exists(nvidia_key_file)
        return {"provider": "nvidia", "present": has_nv}

    # Default fallback check
    if os.path.exists(nvidia_key_file) or os.getenv("NVIDIA_API_KEY"):
        return {"provider": "nvidia", "present": True}

    if os.path.exists(gemini_key_file) or os.getenv("GEMINI_API_KEY"):
        return {"provider": "gemini", "present": True}

    return {"provider": None, "present": False}


@router.post("/key")
def set_key(payload: KeyPayload):
    provider = payload.provider.lower()
    if provider not in ("nvidia", "gemini"):
        raise HTTPException(status_code=400, detail="Unsupported provider")

    api_key = payload.api_key.strip()
    if not api_key:
        raise HTTPException(status_code=400, detail="API key cannot be empty")

    try:
        # Save active provider choice
        with open(active_provider_file, "w") as f:
            f.write(provider)

        if provider == "gemini":
            os.environ["GEMINI_API_KEY"] = api_key
            with open(gemini_key_file, "w") as f:
                f.write(api_key)
            return {"status": "ok", "provider": "gemini"}

        if provider == "nvidia":
            os.environ["NVIDIA_API_KEY"] = api_key
            with open(nvidia_key_file, "w") as f:
                f.write(api_key)
            return {"status": "ok", "provider": "nvidia"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store key: {e}")
