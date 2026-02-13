from fastapi import APIRouter, Depends
from app.services.facade import MLBFacade
from app.api.dependencies import get_facade
from app.api.auth_dependencies import auth_current_user

router = APIRouter(dependencies=[Depends(auth_current_user)]) #<- attaches auth dependency to all routes in this file

@router.get("/milestones")
def milestones_placeholder(facade: MLBFacade = Depends(get_facade)):
    return {"status": "ok"}
# placeholder for the momo
# FastAPI injects the shared facade instance created in app.py via Depends(get_facade)
# endpoints/reading_sessions.py has a mental model check FYI
