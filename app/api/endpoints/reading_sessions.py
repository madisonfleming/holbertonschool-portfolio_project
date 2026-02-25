from fastapi import APIRouter, Depends
from app.services.facade import MLBFacade
from app.api.dependencies import get_facade
from app.api.auth_dependencies import auth_current_user
from app.api.schemas.reading_sessions import CreateReadingSession, ReadingSessionResponse, UpdateReadingSession
from typing import List
from datetime import date

# TODO: if fb uid/user_id not needed to pass to facade - can protect all endpoints at the router level with: router = APIRouter(dependencies=[Depends(auth_current_user)])
router = APIRouter() # note: auth applied at individual endpoint level for now. 

# Requirement: Create a Reading Session
@router.post("/reading-sessions", response_model=ReadingSessionResponse, status_code=201) # note: errors handled at facade/model levels using new error schema
def create_reading_session(
    reading_session_data: CreateReadingSession,
    facade: MLBFacade = Depends(get_facade),
    decoded_token: dict = Depends(auth_current_user) # note: this is the firebase uid for now (may change to user_id later via auth_current_user)
    ):
    firebase_uid = decoded_token["uid"]
    return facade.create_reading_session(reading_session_data, firebase_uid) #TODO: check method name and params match facade

# Requirement: Retrieve reading sessions attached to a child
@router.get("/children/{child_id}/reading-sessions", response_model=List[ReadingSessionResponse], status_code=200)
def get_reading_sessions(
    child_id: str,
    limit: int | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
    facade: MLBFacade = Depends(get_facade),
    decoded_token: dict = Depends(auth_current_user)
    ):
    firebase_uid = decoded_token["uid"]
   
    #TODO: facade may not need firebase uid if looking up sessions attached to child via child_id only. Check method name and params match facade
    return facade.get_reading_sessions(
        child_id=child_id,
        firebase_uid=firebase_uid,
        limit=limit,
        from_date=from_date,
        to_date=to_date)

# Requirement: Update a reading session
@router.put("/reading-sessions/{session_id}", response_model=ReadingSessionResponse, status_code=200)
def update_session(
    session_id: str,
    updated_session_data: UpdateReadingSession,
    facade: MLBFacade = Depends(get_facade),
    decoded_token: dict = Depends(auth_current_user)
    ):
    firebase_uid = decoded_token["uid"]
    #TODO: facade may not need firebase uid if looking up session via session_id only. Check method name and params match facade
    return facade.update_session(session_id, updated_session_data, firebase_uid)

# Requirement: Retrieve reading session counts
@router.get("/children/{child_id}/reading-sessions/count", response_model=int, status_code=200)
def count_reading_sessions(
    child_id: str,
    from_date: date | None = None,
    to_date: date | None = None,
    facade: MLBFacade = Depends(get_facade),
    decoded_token: dict = Depends(auth_current_user)
):
    firebase_uid = decoded_token["uid"]

    return facade.count_reading_sessions(
        child_id=child_id,
        firebase_uid=firebase_uid,
        from_date=from_date,
        to_date=to_date
    )
