from fastapi import APIRouter, Depends
from app.services.facade import MLBFacade
from app.api.dependencies import get_facade

router = APIRouter()

@router.get("/children")
def children_placeholder(facade: MLBFacade = Depends(get_facade)):
    return {"status": "ok"}
# placeholder for the momo
# FastAPI injects the shared facade instance created in app.py via Depends(get_facade)
# endpoints/reading_sessions.py has a mental model check FYI

