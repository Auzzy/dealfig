from dealfig.showcase import app

@app.route("/")
def home():
    return "Hello from Showcase!"