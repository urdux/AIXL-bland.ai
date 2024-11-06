from flask import Flask
from flask_migrate import Migrate, upgrade, migrate, init
from app import create_app, db
import click

app = create_app()
migrate = Migrate(app, db)

# Command line interface for migrations
@app.cli.command("db")
def db_commands():
    """Manage database migrations."""
    pass  # This can be expanded later for more functionality

if __name__ == "__main__":
    app.run(debug=False)
