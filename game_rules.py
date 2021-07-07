class GameRules:
    # possible ball weights
    NORMAL, HEAVIER, LIGHTER = 1000, 1001, 999
    # possible results of a weighing
    LEFT, EQUAL, RIGHT = -1, 0, 1
    ANOMALY_TO_ADJECTIVE = {
        LIGHTER: 'lighter',
        HEAVIER: 'heavier'
    }

    def __init__(self, n_balls, n_weighings, n_anomaly_choices=2):
        assert n_anomaly_choices in (1, 2)
        if n_anomaly_choices == 1:
            anomaly_choices = [self.HEAVIER]
        else:
            anomaly_choices = [self.LIGHTER, self.HEAVIER]
        assert isinstance(n_balls, int) and n_balls >= 2
        assert isinstance(n_weighings, int) and n_weighings >= 1
        if not isinstance(anomaly_choices, list):
            anomaly_choices = list(anomaly_choices)
        assert 1 <= len(anomaly_choices) <= 2
        assert all([ac in [self.LIGHTER, self.HEAVIER] for ac in anomaly_choices])
        self.n_balls = n_balls
        self.n_weighings = n_weighings
        self.anomaly_choices = anomaly_choices

    def get_all_possible_choices(self):
        return [(ball, anomaly) for ball in range(self.n_balls) for anomaly in self.anomaly_choices]

    def describe_game(self, sep='\n', prefix_sep=True, postfix_sep=True):
        if len(self.anomaly_choices) == 2:
            weight_adjective = 'different'
        else:
            weight_adjective = self.ANOMALY_TO_ADJECTIVE[self.anomaly_choices[0]]
        return (sep if prefix_sep else '') + sep.join([
            f'GAME RULES',
            f'There are {self.n_balls} identically looking balls, numbered from 0 to {self.n_balls - 1}, '
            f'but one of them has a slightly {weight_adjective} weight.',
            f'The difference can be noticed only by weighing the balls with a two-plate precision scale.',
            f'Only {self.n_weighings} weighings are allowed, then the right ball and weight must be guessed.'
        ]) + (sep if postfix_sep else '')

    @classmethod
    def tell_heavier_plate(cls, ball_weights, left_plate, right_plate):
        left_weight, right_weight = \
            [sum([ball_weights[ball_index] for ball_index in plate]) for plate in (left_plate, right_plate)]
        if left_weight > right_weight:
            return cls.LEFT
        elif left_weight == right_weight:
            return cls.EQUAL
        else:
            return cls.RIGHT

    @classmethod
    def solution2str(cls, anomaly_index, anomaly):
        return f'the ball nr. {anomaly_index} is {cls.ANOMALY_TO_ADJECTIVE[anomaly]}'
