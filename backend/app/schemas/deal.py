from pydantic import BaseModel
from typing import Optional
from app.models.enums import DealStage

class DealCreate(BaseModel):
    name: str
    company_url: Optional[str] = None
    round: Optional[str] = None
    check_size: Optional[float] = None
    status: Optional[str] = None

class DealOut(BaseModel):
    id: str
    name: str
    stage: DealStage
