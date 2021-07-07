import itertools
import math
import random
from pprint import pprint
from game_rules import GameRules


class GameSolver:
    def __init__(self, game_rules, show_reasoning=False):
        self.game_rules = game_rules
        self._n_balls = self.game_rules.n_balls
        self._balls = tuple(range(self._n_balls))
        self.possible_solutions = [[game_rules.NORMAL if ball != anomaly_index else anomaly
                                    for ball in range(self._n_balls)]
                                   for anomaly_index in range(self._n_balls)
                                   for anomaly in game_rules.anomaly_choices]
        self._recalc_possible_ball_weights()
        self.show_reasoning = show_reasoning

    def _recalc_possible_ball_weights(self):
        self.possible_ball_weights = [set() for _ in range(self._n_balls)]
        for possible_solution in self.possible_solutions:
            for ball, possible_weight in enumerate(possible_solution):
                self.possible_ball_weights[ball].add(possible_weight)
        for ball in range(self._n_balls):
            self.possible_ball_weights[ball] = tuple(sorted(self.possible_ball_weights[ball]))

    def assess_weighing(self, left_plate, right_plate, heavier_plate):
        self.possible_solutions = [ps for ps in self.possible_solutions
                                   if self.game_rules.tell_heavier_plate(ps, left_plate, right_plate) == heavier_plate]
        self._recalc_possible_ball_weights()

    def get_combination_signature(self, balls):
        return tuple(sorted([self.possible_ball_weights[ball] for ball in balls]))

    def get_unique_signature_combinations(self, balls, n_choose, consider_rest=False):
        signature_to_combination = {}
        for combination in itertools.combinations(balls, n_choose):
            signature = self.get_combination_signature(combination)
            if signature in signature_to_combination:
                continue
            if consider_rest:
                rest = tuple([ball for ball in balls if ball not in combination])
                rest_signature = self.get_combination_signature(rest)
                if rest_signature in signature_to_combination:
                    continue
                combination = (combination, rest)
            signature_to_combination[signature] = combination
        return signature_to_combination.values()

    def yield_all_candidate_weighings(self):
        min_unweighed_balls = self._n_balls % 2
        max_unweighed_balls = self._n_balls - 2
        for n_unweighed_balls in range(min_unweighed_balls, max_unweighed_balls + 1, 2):
            n_balls_per_plate = (self._n_balls - n_unweighed_balls) // 2
            for unweighed_balls in self.get_unique_signature_combinations(self._balls, n_unweighed_balls):
                weighed_balls = [ball for ball in self._balls if ball not in unweighed_balls]
                for w in self.get_unique_signature_combinations(weighed_balls, n_balls_per_plate, consider_rest=True):
                    yield w

    def choose_weighing(self, show_reasoning=None):
        def rank_weighing(game_solver, left_plate, right_plate):
            weighing_result_freq = {}
            for ps in game_solver.possible_solutions:
                weighing_result = game_solver.game_rules.tell_heavier_plate(ps, left_plate, right_plate)
                weighing_result_freq[weighing_result] = weighing_result_freq.get(weighing_result, 0) + 1
            descending_freqs = sorted(weighing_result_freq.values(), reverse=True)
            if len(descending_freqs) < 3:
                descending_freqs += [0 for _ in range(3 - len(descending_freqs))]
            return descending_freqs, len(left_plate)

        def scoring2str(weighing, rank, nr=None):
            return f'candidate weighing{" # " + str(nr) if nr else ""}: {weighing[0]} vs. {weighing[1]} ' \
                   f'=> rank: ({rank[0]}, {rank[1]})'

        if show_reasoning is None:
            show_reasoning = self.show_reasoning
        best_rank = ([len(self.possible_solutions)] * 3, self._n_balls + 1)
        best_weighing = None
        best_weighing_nr = None
        if show_reasoning:
            print('--- The solver analyzes all possible weighings with a unique information content:')
        for weighing_nr, (left_plate, right_plate) in enumerate(self.yield_all_candidate_weighings(), 1):
            rank = rank_weighing(self, left_plate, right_plate)
            if show_reasoning:
                print(scoring2str((left_plate, right_plate), rank, weighing_nr))
            if rank < best_rank:
                best_rank = rank
                best_weighing = (left_plate, right_plate)
                best_weighing_nr = weighing_nr
        if show_reasoning:
            print('-- The solver chooses ' + scoring2str(best_weighing, best_rank, best_weighing_nr))
        return best_weighing

    def guess_solution(self, show_reasoning=None):
        if show_reasoning is None:
            show_reasoning = self.show_reasoning
        n_possible_solutions = len(self.possible_solutions)
        if show_reasoning:
            if n_possible_solutions == 1:
                print('The solver has deduced that only one possible solution is left.')
            else:
                print(f'The solver has deduced that there are {n_possible_solutions} possible solutions left.')
                print(f'Therefore, the solver will now try to guess '
                      f'with a chance {1 / n_possible_solutions * 100:.2f}% of winning.')
        attempted_solution = random.choice(self.possible_solutions)
        conviction = 1. / n_possible_solutions
        return self.compact_solution(attempted_solution), conviction

    def compact_solution(self, solution_array):
        normal_weights = [weight == self.game_rules.NORMAL for weight in solution_array]
        anomaly_index = normal_weights.index(False)
        anomaly = solution_array[anomaly_index]
        return anomaly_index, anomaly

    def print_possible_solutions(self):
        n_possible_solutions = len(self.possible_solutions)
        print(f'Now the solver knows that there exist{" these" if n_possible_solutions > 1 else "s this"} '
              f'{n_possible_solutions} possible solution{"s" if n_possible_solutions > 1 else ""}:')
        for anomaly_index, anomaly in sorted([self.compact_solution(possible_solution)
                                              for possible_solution in self.possible_solutions]):
            print(self.game_rules.solution2str(anomaly_index, anomaly))


def test_solver():
    solver = GameSolver(GameRules(12, 3))
    pprint(solver.possible_solutions)
    pprint(solver.possible_ball_weights)
    solver.assess_weighing([0, 1, 2, 3], [4, 5, 6, 7], GameRules.LEFT)
    pprint(solver.possible_solutions)
    pprint(solver.possible_ball_weights)

    solver = GameSolver(GameRules(12, 3))
    solver.assess_weighing([0, 1, 2, 3], [4, 5, 6, 7], GameRules.RIGHT)
    pprint(solver.possible_solutions)
    pprint(solver.possible_ball_weights)

    solver = GameSolver(GameRules(12, 3))
    solver.assess_weighing([0, 1, 2, 3], [4, 5, 6, 7], GameRules.EQUAL)
    pprint(solver.possible_solutions)
    pprint(solver.possible_ball_weights)

    solver = GameSolver(GameRules(12, 3))
    print(solver.rank_weighing([0, 1, 2, 3], [4, 5, 6, 7]))
    print(solver.rank_weighing([0, 1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11]))
    print(solver.rank_weighing([0, 1, 2, 3, 4], [6, 7, 8, 9, 10]))
    print(solver.rank_weighing([0, 1, 2], [6, 7, 8]))
    print(solver.rank_weighing([0, 1, 2], [6, 7, 8, 9]))
    print(solver.get_combination_signature([0, 1, 4, 5, 8, 9]))
    pprint(list(solver.yield_all_candidate_weighings()))
    solver.assess_weighing([0, 1, 2, 3], [4, 5, 6, 7], GameRules.RIGHT)
    print(solver.get_combination_signature([0, 1, 4, 5, 8, 9]))
    pprint(solver.get_unique_signature_combinations([0, 1, 4, 5, 8, 9], 3))
    pprint(solver.get_unique_signature_combinations([0, 1, 4, 5, 8, 9], 3, True))
    pprint(list(solver.yield_all_candidate_weighings()))

    solver = GameSolver(GameRules(13, 3))
    pprint(list(solver.yield_all_candidate_weighings()))
    solver.assess_weighing([0, 1, 2, 3], [4, 5, 6, 7], GameRules.RIGHT)
    pprint(list(solver.yield_all_candidate_weighings()))
    print(solver.choose_weighing(True))


if __name__ == "__main__":
    test_solver()
