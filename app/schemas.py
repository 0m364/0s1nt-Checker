from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

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

class PersonSearch(BaseModel):
    full_name: str
    dob: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class SearchResult(BaseModel):
    source_name: str
    source_type: str
    record_id: Optional[str] = None
    evidence_url: Optional[str] = None
    raw_json: Optional[Dict[str, Any]] = None
    confidence_score: float = 0.0
