from dealfig.config import app

@app.route("/")
def home():
    return "Hello from Config!"