import csv
from .elo import MatchResult


def load_matches(csv_path):
    """Load matches from a CSV file."""
    matches = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            winner = row["team1"] if int(row["team1_score"]) > int(row["team2_score"]) else row["team2"]
            matches.append(
                MatchResult(
                    team1=row["team1"],
                    team2=row["team2"],
                    winner=winner,
                )
            )
    return matches
