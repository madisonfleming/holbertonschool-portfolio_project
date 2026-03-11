from fastapi import APIRouter, Depends
from app.services.facade import MLBFacade
from app.api.dependencies import get_facade
from app.api.auth_dependencies import auth_current_user
from app.api.schemas.reading_sessions import CreateReadingSession, ReadingSessionResponse, UpdateReadingSession
from typing import List
from datetime import date

router = APIRouter()

# Requirement: Create a Reading Session
@router.post("/reading-sessions", response_model=ReadingSessionResponse, status_code=201)
def create_reading_session(
    reading_session_data: CreateReadingSession,
    facade: MLBFacade = Depends(get_facade),
    decoded_token: dict = Depends(auth_current_user)
    ):
    firebase_uid = decoded_token["uid"]
    session = facade.create_reading_session(reading_session_data, firebase_uid)
    return ReadingSessionResponse.from_domain(session)

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
   
    filtered_sessions = facade.get_reading_sessions(
        child_id=child_id,
        firebase_uid=firebase_uid,
        limit=limit,
        from_date=from_date,
        to_date=to_date)

    responses = []
    for session in filtered_sessions:
        r = ReadingSessionResponse.from_domain(session)
        responses.append(r)
    return responses

# Requirement: Update a reading session
@router.put("/reading-sessions/{session_id}", response_model=ReadingSessionResponse, status_code=200)
def update_session(
    session_id: str,
    updated_session_data: UpdateReadingSession,
    facade: MLBFacade = Depends(get_facade),
    decoded_token: dict = Depends(auth_current_user)
    ):
    firebase_uid = decoded_token["uid"]
    session = facade.update_session(session_id, updated_session_data, firebase_uid)
    return ReadingSessionResponse.from_domain(session)

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
    ) # NOTE: no dom obj to schema response obj required (facade return is count, an int)

# additional count function to facilitate heatmap
# returns dict [{date}, {# of reading sessions}]
@router.get(
    "/children/{child_id}/reading-sessions/heatmap",
    response_model=dict[str, int],
    status_code=200
)
def heatmap_reading_sessions(
    child_id: str,
    from_date: date | None = None,
    to_date: date | None = None,
    facade: MLBFacade = Depends(get_facade),
    decoded_token: dict = Depends(auth_current_user)
):
    firebase_uid = decoded_token["uid"]
    return facade.heatmap_count_rs(
        child_id=child_id,
        firebase_uid=firebase_uid,
        from_date=from_date,
        to_date=to_date
    ) #NOTE: no dom obj to schema response obj required (facade return is dict of key=date, val=num sessions logged on date)
