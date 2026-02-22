import os
from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import yaml

class SourcesConfig(BaseModel):
    fbi_most_wanted: bool = True
    ofac_sdn: bool = True
    interpol_red_notices: bool = True
    nsopw: bool = False
    state_police: bool = False
    public_dockets: bool = False
    adverse_media: bool = False
    public_social: bool = False

class RunConfig(BaseModel):
    require_review_score_over: int = 1
    min_confidence_for_auto_score: str = "B"
    cache_ttl_seconds: int = 86400

class RetentionConfig(BaseModel):
    days_to_keep: int = 365
    allow_hard_delete: bool = False

class EmailConfig(BaseModel):
    enabled: bool = False
    smtp_host: str = "smtp.example.com"
    smtp_port: int = 587
    smtp_user: str = "alerts@example.com"
    smtp_password: str = "CHANGE_ME"
    from_address: str = "alerts@example.com"
    to_addresses: List[str] = ["security-team@example.com"]

class AIConfig(BaseModel):
    enabled: bool = False
    provider: str = "openai"
    openai_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    openai_model: str = "gpt-4o"
    gemini_model: str = "gemini-1.5-pro"

class Settings(BaseSettings):
    # App Settings
    PROJECT_NAME: str = "OSINT Threat Scanner"
    VERSION: str = "0.1.0"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = Field(default="postgresql+psycopg2://osint:osint@localhost:5432/osint")

    # Config from YAML
    sources: SourcesConfig = SourcesConfig()
    run: RunConfig = RunConfig()
    retention: RetentionConfig = RetentionConfig()
    email: EmailConfig = EmailConfig()
    ai: AIConfig = AIConfig()

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    @classmethod
    def load_from_yaml(cls, path: str = "config.yaml") -> "Settings":
        if os.path.exists(path):
            with open(path, "r") as f:
                config_data = yaml.safe_load(f) or {}
                # Create settings instance, environment variables will override defaults
                # Then update with YAML data if needed, or pass YAML data to constructor
                # Since pydantic-settings prioritizes env vars, we can mix them.
                # However, for nested models, it's easier to load YAML and then override with env vars if supported.
                # But here, let's keep it simple: load YAML and overlay on top of defaults,
                # but standard BaseSettings doesn't support YAML out of the box easily without extra deps or logic.

                # A simple approach: load yaml, then init Settings with it.
                return cls(**config_data)
        return cls()

settings = Settings.load_from_yaml()
