#===========================================================
# APP NAME HERE
# By YOUR NAME HERE
#===========================================================

from app.helpers.auth import admin_required
from flask import Flask, request, session, render_template, flash, redirect, send_file, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from os import getenv
from io import BytesIO
import html
from app.helpers import *


# Create the app
app = Flask(__name__)


#===========================================================
# App Routes Handlers
#===========================================================

#-----------------------------------------------------------
# Welcome page
#-----------------------------------------------------------
@app.get("/")
def show_welcome():
    return render_template("pages/welcome.jinja")


#-----------------------------------------------------------
# Creature list page - Show all the creatures
#-----------------------------------------------------------
@app.get("/users")
@admin_required
def show_all_users():
    with connect_db() as db:
        sql = """
            SELECT id, forename, lastname, username
            FROM users
        """
        params = ()
        users = db.execute(sql, params).fetchall()

        return render_template("pages/user_list.jinja", users=users)


#-----------------------------------------------------------
# Help page - Show some help
#-----------------------------------------------------------
@app.get("/help")
def show_help():

    flash("Flash test message")
    flash("Flash test message with a longer bit of text")
    flash("Success test message", "success")
    flash("Error test message", "error")

    return render_template("pages/help.jinja")

#-----------------------------------------------------------
# Login page
#-----------------------------------------------------------
@app.get("/")
def show_login():
    return render_template("pages/login.jinja")

#-----------------------------------------------------------
# Handle login form
#-----------------------------------------------------------
@app.post("/login")
def process_login():
    username = request.form.get("username", "").strip().lower()
    password = request.form.get("password", "").strip()

    with connect_db() as db:
        sql = """
                SELECT id, forename, surname, pw_hash, email, icon_file, is_admin
                FROM users
                WHERE username=? 
            """
        params = (username)
        user = db.execute(sql, params).fetchone()

        if not user:
            flash("Unknown User", "error")
            return redirect("/login")
        
        if not check_password_hash(user["pw_hash"], password):
            flash("Incorrect Password", "error")
            return redirect("/login")
        
        if user["admin"]:
            session["admin"] = True

        session["user"] = {
            "id": user["id"],
            "username": username,
            "forename": user["forename"],
            "lastname": user["lastname"],
            "email": user["email"],
            "icon_file": user["icon_file"]
        }

        flash("Login Successful", "success")
        return redirect("/")


#===========================================================
# Configure the app
#===========================================================
load_dotenv()
app.config.from_prefixed_env()
init_logging(app)
init_text_filters(app)
init_date_filters(app)
init_error_handlers(app)
init_database()
register_commands(app)

