import itertools

from flask import render_template, request

from dealfig import data
from dealfig.asset_tracker import app

@app.route("/")
def all():
    exhibitors = data.Exhibitor.get_all()
    return render_template("list-exhibitors.html", exhibitors=exhibitors)

@app.route("/<designer>")
@app.route("/<designer>/info")
def info(designer):
    exhibitor = data.Exhibitor.get_by_designer(designer)
    asset_definitions = data.AssetDefinition.get_by_level(exhibitor.level)

    asset_definition_matches = {}
    unmatched_assets = exhibitor.assets
    for asset_definition in asset_definitions:
        matches, unmatched_assets = data.AssetDefinition.get_matches(asset_definition, unmatched_assets)
        asset_definition_matches[asset_definition] = matches
    
    '''
    missing_assets = []
    collected_assets = {}
    for asset_definition in asset_definitions:
        assets = data.Asset.get_matches_definition(exhibitor.assets, asset_definition)
        if assets:
            collected_assets[asset_definition] = assets
        else:
            missing_assets.append(asset_definition)
    extra_assets = set(exhibitor.assets) - set(itertools.chain.from_iterable(collected_assets.values())).union(missing_assets)
    '''
    
    return render_template("exhibitor-info.html", exhibitor=exhibitor, asset_definition_matches=asset_definition_matches, unmatched_assets=unmatched_assets)