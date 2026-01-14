from sqlalchemy import Column, DateTime, Integer, Text, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base
import uuid

class ICMemo(Base):
    __tablename__ = "ic_memos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    deal_id = Column(UUID(as_uuid=True), ForeignKey("deals.id"), unique=True, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ICMemoVersion(Base):
    __tablename__ = "ic_memo_versions"
    __table_args__ = (UniqueConstraint("memo_id", "version_number"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    memo_id = Column(UUID(as_uuid=True), ForeignKey("ic_memos.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    summary = Column(Text)
    market = Column(Text)
    product = Column(Text)
    traction = Column(Text)
    risks = Column(Text)
    open_questions = Column(Text)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
