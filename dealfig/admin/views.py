from flask import jsonify, redirect, render_template, request, url_for

from dealfig import data
from dealfig.admin import app, forms

@app.route("/")
def home():
    users = data.Users.get_all()
    user_roles = [user_role.role for user_role in data.UserRoles]
    return render_template("home.html", users=users, user_roles=user_roles)

@app.route("/new-user", methods=["POST"])
def new_user():
    user = data.Users.new(request.form["first_name"], request.form["last_name"], request.form["email"], request.form["user_role"])
    return url_for("admin.user_info", username=user.username)

@app.route("/users/delete/", methods=["POST"])
def delete_user():
    return data.Users.delete(request.form["username"])

@app.route("/user/<username>")
def user_info(username):
    user = data.Users.get_by_username(username)
    user_roles = [user_role.role for user_role in data.UserRoles]
    return render_template("user.html", user=user, user_roles=user_roles)

@app.route("/user/<username>/name", methods=["POST"])
def update_user_name(username):
    user = data.Users.update_name(username, request.form["first_name"], request.form["last_name"])
    return jsonify({"first_name": user.first_name, "last_name": user.last_name})

@app.route("/user/<username>/role", methods=["POST"])
def update_user_role(username):
    return data.Users.update_role(username, request.form["value"])

@app.route("/user/<username>/email", methods=["POST"])
def update_user_email(username):
    email = data.Users.update_email(username, request.form["value"])
    return jsonify({"value": email})