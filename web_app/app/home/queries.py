from SPARQLWrapper import SPARQLWrapper, JSON

fuseki_endpoint = "http://localhost:3030/sport_ontology/query"


def get_results(query_statement):
    endpoint = SPARQLWrapper(fuseki_endpoint)
    endpoint.setQuery(query_statement)
    endpoint.setReturnFormat(JSON)
    results = endpoint.query().convert()
    return results


def query_tennis_table(player):
    names = []
    surfaces = []
    start_dates = []
    prizes = []

    query_statement = (
        """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX purl: <http://purl.org/sport/ontology/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?name ?surface ?start ?prize
WHERE {
  ?tournament rdf:type purl:PyramidTournament;
              purl:hasSportType purl:Tennis;
              purl:hasTournamentName ?name;
              dbo:champion ?team;
              purl:hasSurface ?surface;
              dbo:startDateTime ?start;
              purl:hasPrize ?prize.
  ?team dbo:playerInTeam ?player.
  ?player rdf:type dbo:TennisPlayer;
          foaf:name '"""
        + player
        + """'.
}
ORDER BY DESC (?start)
"""
    )
    results = get_results(query_statement)

    for result in results["results"]["bindings"]:
        names.append(result["name"]["value"])
        surfaces.append(result["surface"]["value"])
        start_dates.append(result["start"]["value"].split("T")[0])
        prizes.append(result["prize"]["value"])

    return (names, surfaces, start_dates, prizes)


def query_tennis_bars(player):
    names = []
    no_losses = []

    query_statement = (
        """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX purl: <http://purl.org/sport/ontology/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?name_player_1 (COUNT(?name_player_1) AS ?count)
WHERE {
  ?match rdf:type purl:Match;
         purl:hasHomeTeam ?player1team;
         purl:hasAwayTeam ?player2team;
         purl:hasHomeScore ?home;
         purl:hasAwayScore ?away.
  ?player1team dbo:playerInTeam ?player1.
  ?player1 rdf:type dbo:TennisPlayer;
          foaf:name ?name_player_1.
  ?player2team dbo:playerInTeam ?player2.
  ?player2 rdf:type dbo:TennisPlayer;
           foaf:name '"""
        + player
        + """'.
  FILTER (?home > ?away)
}
GROUP BY ?name_player_1
ORDER BY DESC (?count)
LIMIT 5
"""
    )
    results = get_results(query_statement)

    for result in results["results"]["bindings"]:
        names.append(result["name_player_1"]["value"])
        no_losses.append(result["count"]["value"])

    return (names, no_losses)


def query_tennis_graph(player):
    years = []
    no_cups = []

    query_statement = (
        """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX purl: <http://purl.org/sport/ontology/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?year (COUNT(?tournament) as ?no)
WHERE {
  ?player rdf:type dbo:TennisPlayer;
          foaf:name '"""
        + player
        + """'.
  ?tournament rdf:type purl:PyramidTournament;
              purl:hasSportType purl:Tennis;
              dbo:champion ?team;
              dbo:startDateTime ?date.
  ?team dbo:playerInTeam ?player.
}
GROUP BY (year(?date) as ?year)
ORDER BY ?year
"""
    )
    results = get_results(query_statement)

    for result in results["results"]["bindings"]:
        years.append(result["year"]["value"])
        no_cups.append(result["no"]["value"])

    return (years, no_cups)


query_tennis_table("Ilie Nastase")
query_tennis_bars("Novak Djokovic")
query_tennis_graph("Novak Djokovic")


def query_soccer_table(team, championship, season):
    home_teams = []
    away_teams = []
    home_scores = []
    away_scores = []

    query_statement = (
        """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX purl: <http://purl.org/sport/ontology/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?team_1 ?team_2 ?home ?away
WHERE {
  ?team rdf:type purl:MultiPlayer;
        purl:hasTeamName '"""
        + team
        + """'.
  ?tournament purl:hasSportType purl:Football;
              purl:hasTournamentName '"""
        + championship
        + """';
              dbo:startDateTime ?season.
  {
    ?match rdf:type purl:Match;
         purl:hasTournament ?tournament;
         purl:hasHomeTeam ?team;
         purl:hasAwayTeam ?other;
         purl:hasHomeScore ?home;
         purl:hasAwayScore ?away;
         purl:hasDate ?date.
    ?team purl:hasTeamName ?team_1.
    ?other purl:hasTeamName ?team_2.
  } UNION {
    ?match rdf:type purl:Match;
         purl:hasTournament ?tournament;
         purl:hasAwayTeam ?team;
         purl:hasHomeTeam ?other;
         purl:hasHomeScore ?home;
         purl:hasAwayScore ?away;
         purl:hasDate ?date.
    ?team purl:hasTeamName ?team_2.
    ?other purl:hasTeamName ?team_1.
  }
  FILTER (regex(str(?season), '"""
        + season
        + """', 'i'))
}
ORDER BY ?date
"""
    )
    results = get_results(query_statement)

    for result in results["results"]["bindings"]:
        home_teams.append(result["team_1"]["value"])
        away_teams.append(result["team_2"]["value"])
        home_scores.append(result["home"]["value"])
        away_scores.append(result["away"]["value"])

    return (home_teams, away_teams, home_scores, away_scores)


def query_soccer_bars(manager):
    countries = []
    no_teams = []

    query_statement = (
        """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX purl: <http://purl.org/sport/ontology/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?country (COUNT(?country) as ?no)
WHERE {
  SELECT DISTINCT ?team ?manager ?country
  WHERE {
    ?manager_job rdf:type purl:Transfer;
                 purl:hasPerson ?manager;
                 purl:hasTeam ?team.
    ?manager rdf:type purl:Manager;
             foaf:name '"""
        + manager
        + """'.
    ?team purl:hasClubLocation ?country_uri.
    ?country_uri rdf:type dbo:Country;
             dbo:informationName ?country.
  }
}
GROUP BY ?country
ORDER BY DESC (?no)
"""
    )
    results = get_results(query_statement)

    for result in results["results"]["bindings"]:
        countries.append(result["country"]["value"])
        no_teams.append(result["no"]["value"])

    return (countries, no_teams)


def query_soccer_graph(team, season):
    months = []
    no_goals_for = []
    no_goals_against = []

    query_statement = (
        """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX purl: <http://purl.org/sport/ontology/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?mon (SUM(?score) AS ?for) (SUM (?other) AS ?against)
WHERE {
  {
    ?match rdf:type purl:Match;
           purl:hasTournament ?tournament;
           purl:hasHomeTeam ?team;
           purl:hasHomeScore ?score;
           purl:hasAwayScore ?other;
           purl:hasDate ?date.
    ?tournament dbo:startDateTime ?season.
    ?team purl:hasTeamName '"""
        + team
        + """'.
  }
  UNION
  {
    ?match rdf:type purl:Match;
           purl:hasTournament ?tournament;
           purl:hasAwayTeam ?team;
           purl:hasHomeScore ?other;
           purl:hasAwayScore ?score;
           purl:hasDate ?date.
    ?tournament dbo:startDateTime ?season.
    ?team purl:hasTeamName '"""
        + team
        + """'.
  }
  FILTER (regex(str(?season), '"""
        + season
        + """', "i"))
}
GROUP BY (month(?date) AS ?mon)
"""
    )

    results = get_results(query_statement)

    for result in results["results"]["bindings"]:
        months.append(result["mon"]["value"])
        no_goals_for.append(result["for"]["value"])
        no_goals_against.append(result["against"]["value"])

    return (months, no_goals_for, no_goals_against)
