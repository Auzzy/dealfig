from flask import redirect, render_template, request, url_for

from dealfig import data
from dealfig.benefit_tracker import app


@app.route("/")
@app.route("/list/<event_name>")
def all(event_name=None):
    sponsors = [deal.designer for deal in data.Deals.get_by_event(event_name) if deal.level]
    showcase_designers = [showcase.designer for showcase in data.Showcases.get_by_event(event_name)]
    exhibitors = set(sponsors + showcase_designers)
    return render_template("benefit-tracker.html", exhibitors=exhibitors)

@app.route("/<designer_name>/benefits")
@app.route("/<designer_name>/benefits/<event_name>")
def benefits(designer_name, event_name=None):
    designer = data.Designers.get_by_name(designer_name)
    
    sponsor_benefits = data.Benefits.load(designer.active_deal.level.benefits) if designer.active_deal else data.Benefits()
    showcase_benefits = data.Benefits.load(data.Events.get_by_name(event_name).showcase_benefits) if designer.active_showcase else data.Benefits()
    shared_benefits = sponsor_benefits.intersection(showcase_benefits) if designer.active_deal and designer.active_showcase else data.Benefits()

    benefits = {
        "Sponsor Benefits": sponsor_benefits - shared_benefits,
        "Showcase Benefits": showcase_benefits - shared_benefits,
        "Shared Benefits": shared_benefits
    }
    
    print(sponsor_benefits.image_assets)
    print(sponsor_benefits.text_assets)
    print(showcase_benefits.image_assets)
    print(showcase_benefits.text_assets)
    print(shared_benefits.image_assets)
    print(shared_benefits.text_assets)
    
    return render_template("designer-benefits.html", designer=designer, benefits=benefits)

@app.route("/<designer_name>/benefits/upload_image", methods=["POST"])
def upload_image(designer_name):
    benefit_name = request.form["benefit-name"]
    print(benefit_name)
    for image_asset in request.files.getlist("image-assets"):
        data.BenefitsManager.save_image(designer_name, benefit_name, image_asset)
    return redirect(url_for("benefit_tracker.benefits", designer_name=designer_name))

@app.route("/<designer_name>/benefits/create_preview", methods=["POST"])
def create_preview(designer_name):
    print(request.form["benefit-name"])
    for image_asset in request.files.getlist("image-assets"):
        print(image_asset.filename)
    return ""