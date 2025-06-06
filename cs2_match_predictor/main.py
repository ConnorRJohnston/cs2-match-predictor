import csv
import argparse
from .elo import MatchResult, build_ratings, predict


def load_matches(csv_path):
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


def cli():
    parser = argparse.ArgumentParser(description="Predict CS2 match outcomes using Elo ratings")
    parser.add_argument("dataset", help="Path to CSV dataset of past matches")
    parser.add_argument("team1", help="Name of the first team")
    parser.add_argument("team2", help="Name of the second team")
    args = parser.parse_args()

    matches = load_matches(args.dataset)
    ratings = build_ratings(matches)
    prob = predict(ratings, args.team1, args.team2)
    print(f"Probability that {args.team1} beats {args.team2}: {prob:.2%}")

if __name__ == "__main__":
    cli()
