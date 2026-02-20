# OSINT Threat Scanner (Local MVP)

Local, auditable OSINT scanner for security teams. Runs on Python + Postgres, outputs PDF + XLSX, and enforces human review for scores > 1.

## Features
- **Local CLI + GUI**: Manage cases from command line or web interface.
- **Public Source Connectors**: FBI, OFAC, Interpol.
- **Threat Scoring**: 1–5 scale with confidence tiers.
- **Evidence Logging**: Full audit trail of all searches.
- **Reporting**: Encrypted PDF + XLSX reports.
- **Role-Based Access**: Admin, Analyst, Viewer roles.
- **Professional Grade**: Structured logging, type-safe configuration, and comprehensive testing.

## Quick Start (Docker)

    docker-compose up --build

Open GUI: http://localhost:8000

## Local Development Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Initialize Database**:
    ```bash
    python app/init_db.py
    ```

3.  **Run Application**:
    ```bash
    uvicorn app.main:app --reload
    # OR using Makefile
    make run
    ```

4.  **Run Tests**:
    ```bash
    pytest
    # OR using Makefile
    make test
    ```

## Configuration

Configuration is managed via `config.yaml` and environment variables.

- **config.yaml**: Controls enabled sources, run parameters, retention, and email settings.
- **Environment Variables**: Override defaults or set secrets (e.g. `DATABASE_URL`).

Example `.env`:
```bash
DATABASE_URL=postgresql+psycopg2://osint:osint@localhost:5432/osint
DEBUG=True
```

## Project Structure

- `app/`: Source code
  - `api/`: REST API endpoints
  - `cli/`: CLI commands
  - `connectors/`: External data source integrations
  - `core/`: Core settings and logging
  - `gui/`: Web interface
  - `normalization/`: Data normalization logic
  - `pipeline/`: Data processing pipeline
  - `reports/`: Report generation logic
  - `scoring/`: Threat scoring engine
  - `security/`: Auth and crypto
- `tests/`: Unit and integration tests

## CLI Examples

    python app/cli/cli.py create-case --name "Jane Doe" --dob 1990-01-01 --consent "I consent..."
    python app/cli/cli.py run-case --id <case_id>
    python app/cli/cli.py export-case --id <case_id>

## Legal Disclaimer & Indemnification

This software is intended for educational, research, and authorized security auditing purposes only. The developers of this tool ("the Authors") are not responsible for any misuse or damage caused by this software.

By using this software, you agree to the following terms:

1.  **Authorized Use Only**: You will only use this software on systems and networks for which you have explicit authorization.
2.  **No Liability**: The Authors are not liable for any direct, indirect, incidental, special, exemplary, or consequential damages (including, but not limited to, procurement of substitute goods or services; loss of use, data, or profits; or business interruption) however caused and on any theory of liability, whether in contract, strict liability, or tort (including negligence or otherwise) arising in any way out of the use of this software, even if advised of the possibility of such damage.
3.  **Indemnification**: You agree to indemnify, defend, and hold harmless the Authors from and against any and all claims, liabilities, damages, losses, costs, expenses, or fees (including reasonable attorneys' fees) that such parties may incur as a result of or arising from your (or anyone using your account's) violation of these terms or your use of the software.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
