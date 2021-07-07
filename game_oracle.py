import random
from game_rules import GameRules


class GameOracle:

    RESULT_TO_TEXT = {
        GameRules.LEFT: 'the left plate is heavier',
        GameRules.EQUAL: 'the two plates have the same weight',
        GameRules.RIGHT: 'the right plate is heavier',
    }

    def __init__(self, game_rules, explicit_choice=None):
        self.game_rules = game_rules
        self.n_used_weighings = 0
        if explicit_choice is None:
            self.anomaly_index = random.randrange(0, game_rules.n_balls)
            self.anomaly = random.choice(game_rules.anomaly_choices)
        else:
            assert len(explicit_choice) == 2
            (anomaly_index, anomaly) = explicit_choice
            assert isinstance(anomaly_index, int) and 0 <= anomaly_index < self.game_rules.n_balls
            assert anomaly in (self.game_rules.LIGHTER, self.game_rules.HEAVIER)
            self.anomaly_index = anomaly_index
            self.anomaly = anomaly
        self._weights = [game_rules.NORMAL if i != self.anomaly_index else self.anomaly
                         for i in range(game_rules.n_balls)]

    def tell_heavier_plate(self, left_plate, right_plate):
        assert self.n_used_weighings < self.game_rules.n_weighings
        involved_balls = list(left_plate) + list(right_plate)
        assert len(set(involved_balls)) == len(involved_balls)
        assert all([isinstance(ib, int) and 0 <= ib < self.game_rules.n_balls for ib in involved_balls])
        self.n_used_weighings += 1
        return self.game_rules.tell_heavier_plate(self._weights, left_plate, right_plate)

    def check_guess(self, anomaly_index, anomaly):
        return anomaly_index == self.anomaly_index and anomaly == self.anomaly


def test_oracle():
    n_balls = 12
    n_weighings = 3
    oracle = GameOracle(GameRules(n_balls, n_weighings))
    print(oracle._weights)

    oracle = GameOracle(GameRules(n_balls, n_weighings), (5, GameRules.HEAVIER))
    print(oracle._weights)
    print(oracle.tell_heavier_plate([0, 1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11]))
    print(oracle.tell_heavier_plate([0, 1, 2, 3, 4], [5, 6, 7, 8, 9]))
    print(oracle.tell_heavier_plate([0, 1, 2, 3], [6, 7, 8, 9]))
    try:
        print(oracle.tell_heavier_plate([0, 1, 2], [9, 10, 11]))
    except AssertionError:
        print('limited weighings ok')
    for ball_index in range(n_balls):
        for anomaly in [GameRules.LIGHTER, GameRules.HEAVIER]:
            print(oracle.check_guess(ball_index, anomaly))


if __name__ == "__main__":
    test_oracle()
