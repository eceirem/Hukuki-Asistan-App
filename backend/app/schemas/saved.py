from __future__ import annotations

import uuid
from typing import List

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.case import CaseResponse


class SavedCaseCreate(BaseModel):
    case_id: int = Field(..., gt=0)


class SavedCaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: uuid.UUID
    case_id: int


class SavedCasesList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: List[CaseResponse]
    total: int
