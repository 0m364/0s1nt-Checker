from pydantic import BaseModel
from typing import Optional

class CaseCreate(BaseModel):
    full_name: str
    dob: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    consent_text: str

class ReviewCreate(BaseModel):
    reviewer_name: str
    decision: str
    override_score: Optional[int] = None
    notes: Optional[str] = None
