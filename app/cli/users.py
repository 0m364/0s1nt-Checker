import typer
from app.db import SessionLocal
from app import models
from app.security.auth import hash_password

app = typer.Typer()

@app.command()
def create(username: str, password: str, role: str = "analyst"):
    db = SessionLocal()
    user = models.User(username=username, password_hash=hash_password(password), role=role)
    db.add(user)
    db.commit()
    typer.echo(f"Created user {username} with role {role}")

if __name__ == "__main__":
    app()
