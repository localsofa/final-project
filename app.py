import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request

# Configure application
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///sentences.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        sentences = request.form.get("sentences")
        selected_language = request.form.get("language")
        selected_dialect = request.form.get("dialect")

        if not name or not sentences or not selected_language or not selected_dialect:
            flash("Please fill out all fields.")
            return redirect("/")

        # Add entry into database
        db.execute("INSERT INTO sentences (name, sentences, language, dialect) VALUES (:name, :sentences, :language, :dialect)",
                    name = name, sentences = sentences, language = selected_language, dialect = selected_dialect)

        return redirect("/")

    else:

        # Display entries in index.html
        selected_language = request.args.get("language")
        selected_dialect = request.args.get("dialect")

        rows = db.execute("SELECT * FROM sentences")
        distinct_languages = db.execute("SELECT DISTINCT language FROM sentences")

        # Allow for filtering
        if selected_language:
            distinct_dialects = db.execute("SELECT DISTINCT dialect FROM sentences WHERE language = :language", language = selected_language)
            filtered_rows = [row for row in rows if row["language"] == selected_language]

            # Filter by dialect
            if selected_dialect:
                filtered_rows = [row for row in filtered_rows if row["dialect"] == selected_dialect]


        else:
            distinct_dialects = []
            filtered_rows = rows

        return render_template("index.html", rows = filtered_rows, distinct_languages = distinct_languages, distinct_dialects = distinct_dialects, selected_dialect = selected_dialect)
