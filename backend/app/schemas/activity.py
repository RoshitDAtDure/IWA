from pydantic import BaseModel
from app.models.enums import DealStage

class StageChange(BaseModel):
    to_stage: DealStage
