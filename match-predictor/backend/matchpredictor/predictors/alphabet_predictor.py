from matchpredictor.matchresults.result import Fixture, Outcome
from matchpredictor.predictors.predictor import Prediction, Predictor


class AlphabetPredictor(Predictor):
    def predict(self, fixture: Fixture) -> Prediction:
        if fixture.home_team.name < fixture.away_team.name:
            return Prediction(outcome=Outcome.HOME)
        elif fixture.away_team.name < fixture.home_team.name:
            return Prediction(outcome=Outcome.AWAY)
        else:
            return Prediction(outcome=Outcome.DRAW)
