import datetime

from flask import jsonify, render_template, request, url_for
from werkzeug.exceptions import MethodNotAllowed

from dealfig import data, filters
from dealfig.events import app

DATE_FORMAT = "%m/%d/%Y"

@app.route("/")
def all():
    events = data.Events.get_all()
    return render_template("list-events.html", events=events)

@app.route("/new", methods=["POST"])
def new_event():
    start_date = datetime.datetime.strptime(request.form["start_date"], DATE_FORMAT).date()
    event = data.Events.new(request.form["name"], start_date)
    return jsonify({"redirect": url_for("events.info", event_name=event.name)})

@app.route("/event/<event_name>")
def info(event_name):
    event = data.Events.get(event_name)
    return render_template("event.html", event=event)

@app.route("/event/<event_name>/update_start_date", methods=["POST"])
def update_start_date(event_name):
    start_date = datetime.datetime.strptime(request.form["date"], DATE_FORMAT).date()
    date_str = filters.date_filter(data.Events.update_start_date(event_name, start_date))
    return date_str

@app.route("/event/<event_name>/update_end_date", methods=[])
def update_end_date(event_name):
    end_date = datetime.datetime.strptime(request.form["date"], DATE_FORMAT).date()
    return jsonify({"value": data.Events.update_end_date(event_name, end_date)})

@app.route("/event/<event_name>/update_start_time", methods=[])
def update_start_time(event_name):
    raise MethodNotAllowed([], "The update_start_time endpoint is unimplemented at this time.")

@app.route("/event/<event_name>/update_end_time", methods=[])
def update_end_time(event_name):
    raise MethodNotAllowed([], "The update_end_time endpoint is unimplemented at this time.")

@app.route("/event/<event_name>/update_location", methods=["POST"])
def update_location(event_name):
    return jsonify({"value": data.Events.update_location(event_name, request.form["value"])})

@app.route("/event/<event_name>/update_description", methods=["POST"])
def update_description(event_name):
    return jsonify({"value": data.Events.update_description(event_name, request.form["value"])})