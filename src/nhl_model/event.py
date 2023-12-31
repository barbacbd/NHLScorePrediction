from enum import Enum
from nhl_core import NHLData
from nhl_model.enums import EventType


# List of all shot event types
ShotEvents = [x.value for x in EventType]


class Game:
    def __init__(self, gameId, homeTeamId=None, awayTeamId=None):
        self.gameId = gameId
        self.homeTeamId = homeTeamId
        self.awayTeamId = awayTeamId
        self.homeTeamEvents = []
        self.awayTeamEvents = []

        # Values for prediction and analysis
        self.homeTeamWinPercent = 0.0
        self.awayTeamWinPercent = 0.0
        self.regulationTiePercent = 0.0
        self.homeTeamGoalsPrediction = 0
        self.homeTeamGoalsActual = 0
        self.awayTeamGoalsPrediction = 0
        self.awayTeamGoalsActual = 0

    def addHomeTeamEvent(self, event):
        if event.result.event == EventType.GOAL.value:
            self.homeTeamGoalsActual += 1
        self.homeTeamEvents.append(event)
    
    def addAwayTeamEvent(self, event):
        if event.result.event == EventType.GOAL.value:
            self.awayTeamGoalsActual += 1
        self.awayTeamEvents.append(event)

    @property
    def winnerPredicted(self):
        if (self.homeTeamWinPercent > self.awayTeamWinPercent and \
            self.homeTeamGoalsActual > self.awayTeamGoalsActual) or \
            (self.awayTeamWinPercent > self.homeTeamWinPercent and \
             self.awayTeamGoalsActual > self.homeTeamGoalsActual):
            return True
        return False
    
    @property
    def winner(self):
        return "home" if self.homeTeamGoalsActual > self.awayTeamGoalsActual else "away"

    @property
    def totalGoals(self):
        return self.homeTeamGoalsActual + self.awayTeamGoalsActual

    @property
    def valid(self):
        # technically it is possible to have no events saved, but the team Ids must be present
        return None not in (self.homeTeamId, self.awayTeamId)
    
    def goals(self):
        """Returns a dict of number of goals for each team id for easy calculation
        """
        return {
            self.homeTeamId: self.homeTeamGoalsActual,
            self.awayTeamId: self.awayTeamGoalsActual
        }

    @property
    def json(self):
        return {
            "gameId": self.gameId,
            "homeTeamId": self.homeTeamId,
            "awayTeamId": self.awayTeamId,
            # Missing the actual events. This is too much to load/unload to files
            "homeTeamWinPercent": self.homeTeamWinPercent,
            "awayTeamWinPercent": self.awayTeamWinPercent,
            "regulationTiePercent": self.regulationTiePercent,
            "homeTeamGoalsPrediction": self.homeTeamGoalsPrediction,
            "homeTeamGoalsActual": self.homeTeamGoalsActual,
            "awayTeamGoalsPrediction": self.awayTeamGoalsPrediction,
            "awayTeamGoalsActual": self.awayTeamGoalsActual,
        }

    def fromJson(self, jsonData):
        for key, value in jsonData.items():
            if key in ("homeTeamEvents", "awayTeamEvents"):
                # TODO: this is a massive amount of data, so skipping for now above
                setattr(self, key, [NHLData(x) for x in value])
            else:
                setattr(self, key, value)