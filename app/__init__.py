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
from werkzeug.utils import secure_filename
import uuid
import os

UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads')

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

#-----------------------------------------------------------
# Sign Up page
#-----------------------------------------------------------
@app.get("/users/new")
def show_signup():
    return render_template("pages/sign_up.jinja")

#-----------------------------------------------------------
# Handle user signup
#-----------------------------------------------------------
@app.post("/users/new")
def process_new_user():
    # get text inputs
    forename = request.form.get("forename","").strip()
    lastname = request.form.get("lastname", "").strip()
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    # get image file
    image = request.files.get("image", None)

    if not image or image.filename == "":
        image_filename = "/images/default_icon.png"
    else:
        filename = secure_filename(image.filename)
        random_prefix = uuid.uuid4().hex[:12]
        image_filename = f"{random_prefix}_{filename}"

    filepath = os.path.join(UPLOAD_FOLDER, image_filename)
    image.save(filepath)

    with connect_db as db:
        sql="""
            INSERT INTO users (forename, lastname, username, )
            """



    

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

