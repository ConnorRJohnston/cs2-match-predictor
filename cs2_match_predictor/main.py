import argparse
from .elo import build_ratings, predict
from .data import load_matches


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
