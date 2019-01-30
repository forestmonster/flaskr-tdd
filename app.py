import sqlite3
from flask import (
    Flask,
    request,
    session,
    g,
    redirect,
    url_for,
    abort,
    render_template,
    flash,
    jsonify,
)

# Globals
DATABASE = "flaskr.db"
DEBUG = True
SECRET_KEY = "my_precious"
USERNAME = "admin"
PASSWORD = "admin"

# Initialize app
app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/")
def show_entries():
    """Select all entries from the database, then display them to the user."""
    db = get_db()
    cur = db.execute("SELECT * FROM entries ORDER BY id DESC")
    entries = cur.fetchall()
    return render_template("index.html", entries=entries)


def init_db():
    """Create the database."""
    with app.app_context():
        db = get_db()
        with app.open_resource("schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()


def connect_db():
    """Connect to an existing database."""
    rv = sqlite3.connect(app.config["DATABASE"])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Re-use an existing database if present."""
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Close the database connection."""
    if hasattr(g, "sqlite_db"):
        g.sqlite_db.close()


if __name__ == "__main__":
    init_db()
    app.run()
