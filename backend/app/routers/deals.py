from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.deal import DealCreate
from app.models.deal import Deal
from app.models.enums import DealStage
from app.deps import get_db, require_role

router = APIRouter(prefix="/deals", tags=["deals"])

@router.post("")
def create_deal(
    data: DealCreate,
    user = Depends(require_role("ADMIN", "ANALYST")),
    db: Session = Depends(get_db)
):
    deal = Deal(
        name=data.name,
        company_url=data.company_url,
        owner_id=user.id,
        stage=DealStage.SOURCED,
        round=data.round,
        check_size=data.check_size,
        status=data.status
    )
    db.add(deal)
    db.commit()
    return {"id": deal.id}

@router.get("")
def list_deals(db: Session = Depends(get_db)):
    return db.query(Deal).all()

@router.get("/{deal_id}")
def get_deal(deal_id: str, db: Session = Depends(get_db)):
    deal = db.query(Deal).get(deal_id)
    if not deal:
        raise HTTPException(status_code=404)
    return deal
