from __future__ import annotations

from typing import Annotated, List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import CurrentUser
from app.crud import crud_saved
from app.db.database import get_db
from app.schemas.case import CaseResponse
from app.schemas.saved import SavedCaseResponse
from app.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: CurrentUser) -> UserResponse:
    return UserResponse.model_validate(current_user)


@router.get("/me/saved-cases", response_model=List[CaseResponse])
async def get_saved_cases(
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> List[CaseResponse]:
    cases = await crud_saved.get_user_saved_cases(db, current_user.id)
    return [CaseResponse.model_validate(c) for c in cases]


@router.post(
    "/me/saved-cases/{case_id}",
    response_model=SavedCaseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def save_case(
    case_id: int,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SavedCaseResponse:
    await crud_saved.save_case_for_user(db, current_user.id, case_id)
    return SavedCaseResponse(user_id=current_user.id, case_id=case_id)


@router.delete("/me/saved-cases/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_saved_case(
    case_id: int,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Response:
    await crud_saved.remove_saved_case(db, current_user.id, case_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
