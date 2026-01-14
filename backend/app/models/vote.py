from sqlalchemy import Column, DateTime, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base
from app.models.enums import VoteType
import uuid

class Vote(Base):
    __tablename__ = "votes"
    __table_args__ = (UniqueConstraint("deal_id", "voter_id"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    deal_id = Column(UUID(as_uuid=True), ForeignKey("deals.id"), nullable=False)
    voter_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    vote = Column(Enum(VoteType, name="vote_type"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
