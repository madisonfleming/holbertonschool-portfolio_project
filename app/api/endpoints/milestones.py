from fastapi import APIRouter, Depends
from app.services.facade import MLBFacade
from app.api.dependencies import get_facade
from app.api.auth_dependencies import auth_current_user
from app.api.schemas.milestones import MilestoneResponse
from typing import List

# TODO: if fb uid/user_id not needed to pass to facade - can protect all endpoints at the router level with: router = APIRouter(dependencies=[Depends(auth_current_user)])
router = APIRouter() # NOTE: auth applied at individual endpoint level for now. 

# Requirement: Get ALL milestones
@router.get("/children/{child_id}/milestones", response_model=List[MilestoneResponse], status_code=200)
def get_all_milestones(
    child_id: str,
    facade: MLBFacade = Depends(get_facade),
    decoded_token: dict = Depends(auth_current_user)
    ):
    firebase_uid = decoded_token["uid"]
    return facade.get_all_milestones(child_id, firebase_uid) #TODO: Check method name and params match facade

# Requirement: Get ONE milestone
@router.get("/children/{child_id}/milestones/{milestone_id}", response_model=MilestoneResponse, status_code=200)
def get_one_milestone(
    child_id: str,
    milestone_id: str,
    facade: MLBFacade = Depends(get_facade),
    decoded_token: dict = Depends(auth_current_user)
    ):
    firebase_uid = decoded_token["uid"]
    return facade.get_one_milestone(child_id, milestone_id, firebase_uid) #TODO: Check method name and params match facade
