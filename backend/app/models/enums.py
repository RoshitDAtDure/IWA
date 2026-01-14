import enum

class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    ANALYST = "ANALYST"
    PARTNER = "PARTNER"

class DealStage(str, enum.Enum):
    SOURCED = "SOURCED"
    SCREEN = "SCREEN"
    DILIGENCE = "DILIGENCE"
    IC = "IC"
    INVESTED = "INVESTED"
    PASSED = "PASSED"

class VoteType(str, enum.Enum):
    APPROVE = "APPROVE"
    DECLINE = "DECLINE"
