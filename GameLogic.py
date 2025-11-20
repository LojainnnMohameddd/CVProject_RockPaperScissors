import random

moves = ["rock", "paper", "scissors"]

def random_move():
    """Return random move for the computer."""
    return random.choice(moves)

def decide_winner(player, computer):
    """Returns: player / computer / draw."""
    if player == computer:
        return "draw"

    if (player == "rock" and computer == "scissors") or \
       (player == "paper" and computer == "rock") or \
       (player == "scissors" and computer == "paper"):
        return "player"

    return "computer"

def play_round(player_move):
    """Plays one round. Returns (player_move, computer_move, result)."""
    player_move = player_move.lower()

    if player_move not in moves:
        raise ValueError("Invalid move. Choose: rock, paper, or scissors")

    computer_move = random_move()
    result = decide_winner(player_move, computer_move)

    return player_move, computer_move, result
