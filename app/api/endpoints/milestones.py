from fastapi import APIRouter, Depends
from app.services.facade import MLBFacade
from app.api.dependencies import get_facade
from app.api.auth_dependencies import auth_current_user
from app.api.schemas.milestones import CreateMilestone, MilestoneCompletionResponse
from typing import List

# TODO: if fb uid/user_id not needed to pass to facade - can protect all endpoints at the router level with: router = APIRouter(dependencies=[Depends(auth_current_user)])
router = APIRouter() # NOTE: auth applied at individual endpoint level for now. 


# Requirement: Get ALL milestones, with optional filtering by metric_key
@router.get("/children/{child_id}/milestones", response_model=List[MilestoneCompletionResponse], status_code=200)
def get_all_milestones(
    child_id: str,
    type: str | None = None,
    facade: MLBFacade = Depends(get_facade),
    decoded_token: dict = Depends(auth_current_user)
    ):
    firebase_uid = decoded_token["uid"]

    # if type:
    #     return facade.get_milestones_by_type(child_id, type, firebase_uid)

    # return facade.get_milestones(child_id, firebase_uid)

    if type:
        results = facade.get_milestones_by_type(child_id, type, firebase_uid)
    else:
        results = facade.get_milestones(child_id, firebase_uid)

    milestones = []
    for res in results:
        m = MilestoneCompletionResponse.from_domain(res)
        milestones.append(m)
    return milestones


# Requirement: Get ONE milestone
@router.get("/children/{child_id}/milestones/{milestone_id}", response_model=MilestoneCompletionResponse, status_code=200)
def get_one_milestone(
    child_id: str,
    milestone_id: str,
    facade: MLBFacade = Depends(get_facade),
    decoded_token: dict = Depends(auth_current_user)
    ):
    firebase_uid = decoded_token["uid"]
    milestone = facade.get_milestone(child_id, milestone_id, firebase_uid)
    return MilestoneCompletionResponse.from_domain(milestone)

# Requirement: Complete a weekly milestone
@router.post("/children/{child_id}/milestones", response_model=MilestoneCompletionResponse, status_code=201)
def complete_weekly_milestone(
    data: CreateMilestone,
    facade: MLBFacade = Depends(get_facade),
    decoded_token: dict = Depends(auth_current_user)
    ):
    firebase_uid = decoded_token["uid"]
    milestone = facade.create_weekly_milestone(data, firebase_uid)
    return MilestoneCompletionResponse.from_domain(milestone)