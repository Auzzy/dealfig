from dealfig.assets import app

@app.route("/")
def home():
    return "Hello from Assets!"