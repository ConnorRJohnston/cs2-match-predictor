import csv
from .elo import MatchResult


def load_matches(csv_path):
    """Load matches from a CSV file.

    The function supports two formats:
    - ``team1,team2,team1_score,team2_score`` (sample dataset)
    - ``team1,team2,team1score,team2score`` (HLTV dataset)
    """
    matches = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)

        if {"team1_score", "team2_score"}.issubset(reader.fieldnames):
            team1_key = "team1_score"
            team2_key = "team2_score"
        elif {"team1score", "team2score"}.issubset(reader.fieldnames):
            team1_key = "team1score"
            team2_key = "team2score"
        else:
            raise ValueError("CSV missing required score columns")

        for row in reader:
            winner = row["team1"] if int(row[team1_key]) > int(row[team2_key]) else row["team2"]
            matches.append(
                MatchResult(
                    team1=row["team1"],
                    team2=row["team2"],
                    winner=winner,
                )
            )
    return matches
