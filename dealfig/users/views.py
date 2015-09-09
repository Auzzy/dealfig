from dealfig.users import app

@app.route("/")
def home():
    return "Hello from Users!"

@app.route("/<username>")
@app.route("/info/<username>")
def info(username):
    return username + " INFO"