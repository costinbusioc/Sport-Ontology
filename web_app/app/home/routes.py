# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint, queries
from flask import render_template, request


@blueprint.route("/sparql", methods=["GET", "POST"])
def sparql():
    result = ""
    data = {}
    if request.method == "POST":
        try:
            query = request.form.get("query")
            results = queries.get_results(query)

            keys = results["head"]["vars"]
            for key in keys:
                data[key] = []
            for result in results["results"]["bindings"]:
                for key in keys:
                    data[key].append(result[key]['value'])
        except:
            pass

    return render_template("sparql.html", data=data)


@blueprint.route("/tennis-table-chart", methods=["GET", "POST"])
def tennis_table():
    name = ""
    tournaments = []
    surfaces = []
    start_dates = []
    prizes = []

    if request.method == "POST":
        name = request.form.get("name")
        tournaments, surfaces, start_dates, prizes = queries.query_tennis_table(name)

    return render_template(
        "tennis-table-chart.html",
        name=name,
        tournaments=tournaments,
        surfaces=surfaces,
        start_dates=start_dates,
        prizes=prizes,
    )


@blueprint.route("/tennis-bar-chart", methods=["GET", "POST"])
def tennis_bar():
    data = {}
    if request.method == "POST":
        name = request.form.get("name")
        players, nr_loses = queries.query_tennis_bars(name)

        data = {
            'name': name,
            'players': players,
            'nr_loses': nr_loses,
            'total': sum([int(x) for x in nr_loses])
        }

    return render_template("tennis-bar-chart.html", data=data)


@blueprint.route("/tennis-graph-chart", methods=["GET", "POST"])
def tennis_graph():
    data = {}
    if request.method == "POST":
        name = request.form.get("name")
        years, nr_cups = queries.query_tennis_graph(name)

        data = {
            'name': name,
            'years': years,
            'nr_cups': nr_cups,
            'total': sum([int(x) for x in nr_cups])
        }

    return render_template("tennis-graph-chart.html", data=data)


@blueprint.route("/soccer-table-chart", methods=["GET", "POST"])
def soccer_table():
    team = ""
    tournament = ""
    season = ""
    home_teams = []
    away_teams = []
    home_scores = []
    away_scores = []

    if request.method == "POST":
        team = request.form.get("team")
        tournament = request.form.get("tournament")
        season = request.form.get("season")
        start_year = season.split('-')[0]

        home_teams, away_teams, home_scores, away_scores = queries.query_soccer_table(
            team, tournament, start_year
        )

    return render_template(
        "soccer-table-chart.html",
        team=team,
        tournament=tournament,
        season=season,
        home_teams=home_teams,
        away_teams=away_teams,
        home_scores=home_scores,
        away_scores=away_scores,
    )


@blueprint.route("/soccer-bar-chart", methods=["GET", "POST"])
def soccer_bar():
    data = {}

    if request.method == "POST":
        name = request.form.get("name")
        countries, nr_teams = queries.query_soccer_bars(name)
        total = sum([int(x) for x in nr_teams])
        data = {
            'name': name,
            'countries': countries,
            'nr_teams': nr_teams,
            'total': total
        }

    return render_template("soccer-bar-chart.html", data=data)


@blueprint.route("/soccer-graph-chart", methods=["GET", "POST"])
def soccer_graph():
    data = {}
    if request.method == "POST":
        team = request.form.get("team")
        season = request.form.get("season")
        start_year = season.split('-')[0]
        months, goals_for, goals_against = queries.query_soccer_graph(team, start_year)

        months_dict = {
            '01': 'JAN',
            '02': 'FEB',
            '03': 'MAR',
            '04': 'APR',
            '05': 'MAY',
            '06': 'JUN',
            '07': 'JUL',
            '08': 'AUG',
            '09': 'SEP',
            '10': 'OCT',
            '11': 'NOV',
            '12': 'DEC'
        }
        months = [months_dict[x] for x in months]

        data = {
            'team': team,
            'season': season,
            'months': months,
            'goals_for': goals_for,
            'goals_against': goals_against
        }
    return render_template("soccer-graph-chart.html", data=data)
