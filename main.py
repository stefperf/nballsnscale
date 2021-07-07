from game_rules import GameRules
from game_oracle import GameOracle
from game_solver import GameSolver
from pprint import pprint


def play_game(rules, explicit_choice=None, show_rules=True, show_game=True, show_reasoning=False):

    def plate2str(plate):
        return 'ball' + ('s ' + str(plate) if len(plate) > 1 else ' ' + str(plate[0]))

    if show_rules: print(rules.describe_game())

    oracle = GameOracle(rules, explicit_choice)
    if show_game: print(f'This is the {"randomly" if explicit_choice else "explicitly"} chosen secret solution:\n'
          f'{rules.solution2str(oracle.anomaly_index, oracle.anomaly)}.')
    if show_game: print(f'')

    solver = GameSolver(rules)
    if show_reasoning: solver.print_possible_solutions()

    for weighing_nr in range(1, rules.n_weighings + 1):
        if show_game: print(f'Weighting nr. {weighing_nr}:')
        (left_plate, right_plate) = solver.choose_weighing(show_reasoning)
        if show_game: print(f'The solver puts the {plate2str(left_plate)} on the left plate '
                       f'and the {plate2str(right_plate)} on the right plate.')
        heavier_plate = oracle.tell_heavier_plate(left_plate, right_plate)
        if show_game: print(f'The oracle reveals that {oracle.RESULT_TO_TEXT[heavier_plate]}.')
        solver.assess_weighing(left_plate, right_plate, heavier_plate)
        if show_reasoning: solver.print_possible_solutions()
        print(f'')

    ((guessed_anomaly_index, guessed_anomaly), guess_conviction) = solver.guess_solution(show_reasoning)
    if show_game: print(f'The solver states that {rules.solution2str(guessed_anomaly_index, guessed_anomaly)}.')
    guess_is_correct = oracle.check_guess(guessed_anomaly_index, guessed_anomaly)
    if show_game: print(f'The oracle reveals that the solver has {"won" if guess_is_correct else "lost"} this game.')
    if show_game: print(f'')
    
    return guess_is_correct, guess_conviction


def analyze_game(rules, show_games=True):
    print()
    print('=' * 120)
    all_possible_choices = rules.get_all_possible_choices()
    n_games = len(all_possible_choices)
    print(f'ANALYZING ALL {n_games} POSSIBLE GAMES WITH THE GIVEN RULES:')
    print(rules.describe_game())
    print(f'')
    n_victories = 0
    total_conviction = 0.
    for game_nr, choice in enumerate(all_possible_choices, 1):
        show_reasoning = True if game_nr == 1 else False
        print('-' * 120)
        print(f'Playing game {game_nr} / {n_games}'
              f'{", showing the reasoning made by the solver" if show_reasoning else ""}...')
        game_won, guess_conviction = play_game(
            rules, explicit_choice=choice, show_rules=False, show_game=show_games, show_reasoning=show_reasoning
        )
        n_victories += 1 if game_won else 0
        total_conviction += guess_conviction
    average_conviction = total_conviction / n_games
    print(f'')
    print(f'THE SOLVER WON {n_victories} / {n_games} GAMES. '
          f'ON AVERAGE, THE SOLVER WAS {average_conviction * 100:.2f}% SURE OF ITS GUESS.')
    print('=' * 120)
    print(f'')


if __name__ == "__main__":
    analyze_game(GameRules(n_balls=12, n_weighings=3, n_anomaly_choices=2))
    analyze_game(GameRules(n_balls=13, n_weighings=3, n_anomaly_choices=2))
