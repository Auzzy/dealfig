from dealfig.deals import app

@app.route("/")
def home():
    return "Hello from Deals!"