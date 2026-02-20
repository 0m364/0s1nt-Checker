import uuid
from sqlalchemy import Column, String, Date, DateTime, Integer, Numeric, Text, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db import Base

class Person(Base):
    __tablename__ = "persons"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=False)
    dob = Column(Date)
    address = Column(Text)
    email = Column(String)
    phone = Column(String)
    created_at = Column(DateTime, server_default=func.now())

class Consent(Base):
    __tablename__ = "consents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    person_id = Column(UUID(as_uuid=True), ForeignKey("persons.id"))
    consent_text = Column(Text, nullable=False)
    consented_at = Column(DateTime, server_default=func.now())
    ip_address = Column(String)
    user_agent = Column(String)

class Case(Base):
    __tablename__ = "cases"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    person_id = Column(UUID(as_uuid=True), ForeignKey("persons.id"))
    status = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

class Input(Base):
    __tablename__ = "inputs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey("cases.id"))
    input_json = Column(JSON, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class Evidence(Base):
    __tablename__ = "evidence"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey("cases.id"))
    source_name = Column(String, nullable=False)
    source_type = Column(String, nullable=False)
    record_id = Column(String)
    evidence_url = Column(Text)
    found_at = Column(DateTime, server_default=func.now())
    raw_json = Column(JSON)

class Match(Base):
    __tablename__ = "matches"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey("cases.id"))
    evidence_id = Column(UUID(as_uuid=True), ForeignKey("evidence.id"))
    match_tier = Column(String, nullable=False)
    confidence_score = Column(Numeric(5, 2), nullable=False)
    match_notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

class Score(Base):
    __tablename__ = "scores"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey("cases.id"))
    computed_score = Column(Integer, nullable=False)
    confidence_tier = Column(String, nullable=False)
    rationale = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

class Review(Base):
    __tablename__ = "reviews"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey("cases.id"))
    reviewer_name = Column(String, nullable=False)
    decision = Column(String, nullable=False)
    override_score = Column(Integer)
    notes = Column(Text)
    reviewed_at = Column(DateTime, server_default=func.now())

class AuditEvent(Base):
    __tablename__ = "audit_events"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey("cases.id"))
    event_type = Column(String, nullable=False)
    event_data = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())

class Report(Base):
    __tablename__ = "reports"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey("cases.id"))
    pdf_path = Column(Text)
    xlsx_path = Column(Text)
    generated_at = Column(DateTime, server_default=func.now())
    file_hash = Column(String)

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class Session(Base):
    __tablename__ = "sessions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    token = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime, nullable=False)

class AccessLog(Base):
    __tablename__ = "access_logs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    route = Column(String, nullable=False)
    method = Column(String, nullable=False)
    status_code = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class Explainability(Base):
    __tablename__ = "explainability"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey("cases.id"))
    summary = Column(Text)
    evidence_reasons = Column(JSON)
    conflicts = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
