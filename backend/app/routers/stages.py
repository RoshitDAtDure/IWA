from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.activity import StageChange
from app.models.deal import Deal
from app.models.activity import Activity
from app.deps import get_db, require_role

router = APIRouter(prefix="/deals", tags=["stages"])

@router.patch("/{deal_id}/stage")
def change_stage(
    deal_id: str,
    data: StageChange,
    user = Depends(require_role("ADMIN", "ANALYST")),
    db: Session = Depends(get_db)
):
    deal = db.query(Deal).get(deal_id)
    if not deal:
        raise HTTPException(status_code=404)

    old = deal.stage
    deal.stage = data.to_stage

    activity = Activity(
        deal_id=deal.id,
        actor_id=user.id,
        message=f"{user.email} moved deal from {old} to {data.to_stage}",
        from_stage=old,
        to_stage=data.to_stage
    )

    db.add(activity)
    db.commit()
    return {"ok": True}
