import datetime

from flask import render_template, request

from dealfig import data
from dealfig.deals import app


DATE_FORMAT = "%m/%d/%Y"


@app.route("/")
def all():
    return render_template("list-deals.html", deals=data.Deals.get_all())

@app.route("/<designer>")
@app.route("/<designer>/info")
def info(designer):
    deal = data.Deals.get_by_designer(designer)
    return render_template("deal-info.html", deal=deal)

@app.route("/<designer>/contract/sent", methods=["POST"])
def contract_sent(designer):
    date_str = request.form["date"]
    contract = _save_date(designer, date_str, data.Contract.save_sent)
    return contract.sent.strftime(DATE_FORMAT)

@app.route("/<designer>/contract/signed", methods=["POST"])
def contract_signed(designer):
    date_str = request.form["date"]
    contract = _save_date(designer, date_str, data.Contract.save_signed)
    return contract.signed.strftime(DATE_FORMAT)

@app.route("/<designer>/invoice/sent", methods=["POST"])
def invoice_sent(designer):
    date_str = request.form["date"]
    invoice = _save_date(designer, date_str, data.Invoice.save_sent)
    return invoice.sent.strftime(DATE_FORMAT)

@app.route("/<designer>/invoice/paid", methods=["POST"])
def invoice_paid(designer):
    date_str = request.form["date"]
    invoice = _save_date(designer, date_str, data.Invoice.save_paid)
    return invoice.paid.strftime(DATE_FORMAT)

def _save_date(designer, date_str, save_func):
    deal = data.Deals.get_by_designer(designer)
    date = datetime.datetime.strptime(date_str, DATE_FORMAT).date()
    return save_func(deal, date)