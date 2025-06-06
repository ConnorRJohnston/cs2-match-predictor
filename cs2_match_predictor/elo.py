# Simple Elo rating system for CS2 match predictions
from dataclasses import dataclass
from typing import Dict, Iterable

K_FACTOR = 32
START_RATING = 1500

@dataclass
class MatchResult:
    team1: str
    team2: str
    winner: str  # name of the winning team

def expected_score(rating_a: float, rating_b: float) -> float:
    """Compute expected score for team A."""
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

def update_ratings(ratings: Dict[str, float], match: MatchResult) -> None:
    """Update Elo ratings based on a single match result."""
    r1 = ratings.get(match.team1, START_RATING)
    r2 = ratings.get(match.team2, START_RATING)

    expected1 = expected_score(r1, r2)
    expected2 = expected_score(r2, r1)

    score1 = 1 if match.winner == match.team1 else 0
    score2 = 1 if match.winner == match.team2 else 0

    ratings[match.team1] = r1 + K_FACTOR * (score1 - expected1)
    ratings[match.team2] = r2 + K_FACTOR * (score2 - expected2)

def build_ratings(matches: Iterable[MatchResult]) -> Dict[str, float]:
    """Build ratings from a list of match results."""
    ratings: Dict[str, float] = {}
    for match in matches:
        update_ratings(ratings, match)
    return ratings

def predict(ratings: Dict[str, float], team1: str, team2: str) -> float:
    """Predict probability that team1 beats team2."""
    r1 = ratings.get(team1, START_RATING)
    r2 = ratings.get(team2, START_RATING)
    return expected_score(r1, r2)
