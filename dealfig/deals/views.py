import datetime

from flask import jsonify, redirect, render_template, request, url_for

from dealfig import data, filters
from dealfig.deals import app

DATE_FORMAT = "%m/%d/%Y"

@app.route("/")
@app.route("/list/<year>")
def all(year=None):
    return render_template("list-deals.html", deals=data.Deals.get_by_year(year))

@app.route("/<designer>/create", methods=["POST"])
def create(designer):
    deal = data.Deals.get_or_create(designer)
    return redirect(url_for('deals.info', designer=designer))

@app.route("/<designer>/")
@app.route("/<designer>/<year>")
def info(designer, year=None):
    deal = data.Deals.get_by_designer(designer, year)
    owner_list = data.Users.get_all()
    level_list = data.DealLevels.get_all()
    return render_template("deal-info.html", deal=deal, owner_list=owner_list, level_list=level_list)

@app.route("/<designer>/owner", methods=["POST"])
def update_owner(designer):
    return data.Deals.update_owner(designer, request.form["value"])

@app.route("/<designer>/level", methods=["POST"])
def update_level(designer):
    return data.Deals.update_level(designer, request.form["value"])

@app.route("/<designer>/cash", methods=["POST"])
def update_cash(designer):
    cash = data.Deals.update_cash(designer, request.form["value"])
    return jsonify({"value": cash})

@app.route("/<designer>/inkind", methods=["POST"])
def update_inkind(designer):
    inkind = data.Deals.update_inkind(designer, request.form["value"])
    return jsonify({"value": inkind})

@app.route("/<designer>/notes", methods=["POST"])
def update_notes(designer):
    notes = data.Deals.update_notes(designer, request.form["value"])
    return jsonify({"value": notes})

@app.route("/<designer>/contract/sent", methods=["POST"])
def contract_sent(designer):
    date_str = request.form["date"]
    return _save_date(designer, date_str, data.Contract.save_sent)

@app.route("/<designer>/contract/signed", methods=["POST"])
def contract_signed(designer):
    date_str = request.form["date"]
    return _save_date(designer, date_str, data.Contract.save_signed)

@app.route("/<designer>/invoice/sent", methods=["POST"])
def invoice_sent(designer):
    date_str = request.form["date"]
    return _save_date(designer, date_str, data.Invoice.save_sent)

@app.route("/<designer>/invoice/paid", methods=["POST"])
def invoice_paid(designer):
    date_str = request.form["date"]
    return _save_date(designer, date_str, data.Invoice.save_paid)

def _save_date(designer, date_str, save_func):
    date = datetime.datetime.strptime(date_str, DATE_FORMAT).date()
    saved_date = save_func(designer, date)
    return filters.date_filter(saved_date)