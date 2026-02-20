# OSINT Threat Scanner (Local MVP)

Local, auditable OSINT scanner for security teams. Runs on Python + Postgres, outputs PDF + XLSX, and enforces human review for scores > 1.

## Features
- Local CLI + GUI
- Public source connectors (FBI, OFAC, Interpol)
- Threat scoring 1–5 with confidence tiers
- Evidence logging + audit trail
- PDF + XLSX reporting
- Role-based access (Admin/Analyst/Viewer)

## Quick Start (Docker)

    docker-compose up --build

Open GUI: http://localhost:8000

## Local Run (No Docker)

    pip install -r requirements.txt
    python app/init_db.py
    uvicorn app.main:app --reload

## CLI Examples

    python app/cli/cli.py create-case --name "Jane Doe" --dob 1990-01-01 --consent "I consent..."
    python app/cli/cli.py run-case --id <case_id>
    python app/cli/cli.py export-case --id <case_id>

## Config
config.yaml controls enabled sources.

## License
Internal / Restricted use only.
