from typing import Dict, Iterable

from matchpredictor.matchresults.result import Fixture, Outcome, Result, Team
from matchpredictor.predictors.predictor import Predictor, Prediction

DEFAULT_RATING = 1500.0

class EloRatings:
    def __init__(self, k_factor: float = 20.0, home_advantage: float = 40.0) -> None:
        self.k_factor = k_factor
        self.home_advantage = home_advantage
        self.ratings: Dict[Team, float] = {}

    def rating_for(self, team: Team) -> float:
        return self.ratings.get(team, DEFAULT_RATING)

    def record_result(self, result: Result) -> None:
        home_team = result.fixture.home_team
        away_team = result.fixture.away_team

        home_rating = self.rating_for(home_team)
        away_rating = self.rating_for(away_team)

        expected_home = self.__expected_home_score(home_rating, away_rating)
        actual_home = self.__actual_home_score(result.outcome)

        goal_difference = abs(result.home_goals - result.away_goals)
        change = self.k_factor * self.__margin_multiplier(goal_difference) * (actual_home - expected_home)

        self.ratings[home_team] = home_rating + change
        self.ratings[away_team] = away_rating - change

    def __expected_home_score(self, home_rating: float, away_rating: float) -> float:
        rating_diff = away_rating - (home_rating + self.home_advantage)
        return 1 / (1 + 10 ** (rating_diff / 400))

    @staticmethod
    def __actual_home_score(outcome: Outcome) -> float:
        if outcome == Outcome.HOME:
            return 1.0
        elif outcome == Outcome.AWAY:
            return 0.0
        else:
            return 0.5

    @staticmethod
    def __margin_multiplier(goal_difference: int) -> float:
        if goal_difference <= 1:
            return 1.0
        elif goal_difference == 2:
            return 1.5
        else:
            return (11 + goal_difference) / 8


class EloPredictor(Predictor):
    def __init__(self, ratings: EloRatings, draw_margin: float = 0.0) -> None:
        self.ratings = ratings
        self.draw_margin = draw_margin

    def predict(self, fixture: Fixture) -> Prediction:
        home_rating = self.ratings.rating_for(fixture.home_team) + self.ratings.home_advantage
        away_rating = self.ratings.rating_for(fixture.away_team)

        difference = home_rating - away_rating

        if difference > self.draw_margin:
            return Prediction(outcome=Outcome.HOME)
        elif difference < -self.draw_margin:
            return Prediction(outcome=Outcome.AWAY)
        else:
            return Prediction(outcome=Outcome.DRAW)


def calculate_elo_ratings(
        results: Iterable[Result],
        k_factor: float = 20.0,
        home_advantage: float = 40.0,
) -> EloRatings:
    ratings = EloRatings(k_factor=k_factor, home_advantage=home_advantage)

    for result in results:
        ratings.record_result(result)

    return ratings


def train_elo_predictor(
        results: Iterable[Result],
        k_factor: float = 20.0,
        home_advantage: float = 40.0,
        draw_margin: float = 0.0,
) -> Predictor:
    ratings = calculate_elo_ratings(results, k_factor=k_factor, home_advantage=home_advantage)

    return EloPredictor(ratings, draw_margin=draw_margin)
