from flask import jsonify, redirect, render_template, request, url_for

from dealfig import data
from dealfig.admin import app

@app.route("/")
def home():
    users = data.Users.get_all()
    user_roles = [user_role.name for user_role in data.UserRoles.get_all()]
    return render_template("admin.html", users=users, user_roles=user_roles)

@app.route("/new-user", methods=["POST"])
def new_user():
    print(request.form.getlist("user_role"))
    user = data.Users.new(request.form["first_name"], request.form["last_name"], request.form["email"], request.form["user_role"])
    return jsonify({"redirect": url_for("admin.user_info", username=user.username)})

@app.route("/users/delete/", methods=["POST"])
def delete_user():
    return data.Users.delete(request.form["username"])

@app.route("/user/<username>")
def user_info(username):
    user = data.Users.get_by_username(username)
    user_roles = [user_role.name for user_role in data.UserRoles.get_all()]
    return render_template("user.html", user=user, user_roles=user_roles)

@app.route("/user/<username>/name", methods=["POST"])
def update_user_name(username):
    user = data.Users.update_name(username, request.form["first_name"], request.form["last_name"])
    return jsonify({"first_name": user.first_name, "last_name": user.last_name})

@app.route("/user/<username>/role", methods=["POST"])
def update_user_roles(username):
    role_names = data.Users.update_roles(username, request.form.getlist("roles"))
    return jsonify({"roles": role_names})

@app.route("/user/<username>/email", methods=["POST"])
def update_user_email(username):
    email = data.Users.update_email(username, request.form["value"])
    return jsonify({"value": email})