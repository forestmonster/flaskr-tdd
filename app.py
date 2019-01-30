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
def index():
    """Select all entries from the database, then display them to the user."""
    db = get_db()
    cur = db.execute("SELECT * FROM entries ORDER BY id DESC")
    entries = cur.fetchall()
    return render_template("index.html", entries=entries)


@app.route("/login", methods=["GET", "POST"])
def login():
    """User login / auth / session management."""
    error = None
    if request.method == "POST":
        if request.form["username"] != app.config["USERNAME"]:
            error = "Invalid username"
        elif request.form["password"] != app.config["PASSWORD"]:
            error = "Invalid password"
        else:
            session["logged_in"] = True
            flash("You were logged in.")
            return redirect(url_for("index"))
        return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    """User logout / auth / session management."""
    session.pop("logged_in", None)
    flash("You were logged out")
    return redirect(url_for("index"))


@app.route('/add', methods=['POST'])
def add_entry():
    """Add new post to database."""
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute(
        'INSERT INTO entries (title, text) VALUES (?, ?)',
        [request.form['title'], request.form['text']]
    )
    db.commit()
    flash('New entry was successfully posted.')
    return redirect(url_for('index'))

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
