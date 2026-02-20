import typer
import requests

app = typer.Typer()
API_URL = "http://localhost:8000/api"

@app.command()
def create_case(name: str, dob: str = "", address: str = "", email: str = "", phone: str = "", consent: str = ""):
    payload = {"full_name": name, "dob": dob, "address": address, "email": email, "phone": phone, "consent_text": consent}
    r = requests.post(f"{API_URL}/cases", json=payload)
    typer.echo(r.json())

@app.command()
def run_case(case_id: str):
    r = requests.post(f"{API_URL}/cases/{case_id}/run")
    typer.echo(r.json())

@app.command()
def export_case(case_id: str):
    r = requests.post(f"{API_URL}/cases/{case_id}/report")
    typer.echo(r.json())

if __name__ == "__main__":
    app()
