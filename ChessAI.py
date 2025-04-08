"""
Handling the AI moves.
"""
import random
import time

piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}

knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
               [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
               [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

piece_position_scores = {"wN": knight_scores,
                         "bN": knight_scores[::-1],
                         "wB": bishop_scores,
                         "bB": bishop_scores[::-1],
                         "wQ": queen_scores,
                         "bQ": queen_scores[::-1],
                         "wR": rook_scores,
                         "bR": rook_scores[::-1],
                         "wp": pawn_scores,
                         "bp": pawn_scores[::-1]}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3
# 

class Node:
    def __init__(self, game_state, parent=None):
        self.game_state = game_state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0

    def is_fully_expanded(self):
        return len(self.children) == len(self.game_state.getValidMoves())

    def best_child(self, exploration_weight=1.4):
        """
        Select the best child node using the UCT formula.
        """
        return max(self.children, key=lambda child: child.value / (child.visits + 1) +
                   exploration_weight * (2 * (self.visits + 1)) ** 0.5)


def findBestMoveMCTS(game_state, valid_moves, simulations=1000):
    """
    Finds the best move using Monte Carlo Tree Search (MCTS).
    """
    root = Node(game_state)

    for _ in range(simulations):
        node = root
        # Selection
        while node.is_fully_expanded() and node.children:
            node = node.best_child()

        # Expansion
        if not node.is_fully_expanded():
            move = random.choice([m for m in game_state.getValidMoves() if m not in [child.game_state.move_log[-1] for child in node.children]])
            game_state.makeMove(move)
            child_node = Node(game_state, parent=node)
            node.children.append(child_node)
            game_state.undoMove()
            node = child_node

        # Simulation
        value = simulate_random_game(node.game_state)

        # Backpropagation
        backpropagate(node, value)

    # Return the best move from the root node
    return root.best_child(exploration_weight=0).game_state.move_log[-1]


def simulate_random_game(game_state):
    """
    Simulates a random game from the given game state and returns the result.
    """
    while not game_state.checkmate and not game_state.stalemate:
        moves = game_state.getValidMoves()
        if not moves:
            break
        move = random.choice(moves)
        game_state.makeMove(move)
    if game_state.checkmate:
        return -1 if game_state.white_to_move else 1
    return 0


def backpropagate(node, value):
    """
    Backpropagates the simulation result up the tree.
    """
    while node:
        node.visits += 1
        node.value += value
        node = node.parent
# 

def findBestMove(game_state, valid_moves, return_queue):
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    findMoveNegaMaxAlphaBeta(game_state, valid_moves, DEPTH, -CHECKMATE, CHECKMATE,
                             1 if game_state.white_to_move else -1)
    return_queue.put(next_move)


def findMoveNegaMaxAlphaBeta(game_state, valid_moves, depth, alpha, beta, turn_multiplier, null_move_allowed=True):
    global next_move
    if depth == 0:
        return turn_multiplier * scoreBoard(game_state)

    # Null Move Heuristic
    if null_move_allowed and depth >= 3 and not game_state.inCheck():
        game_state.white_to_move = not game_state.white_to_move  # Switch turn to simulate null move
        null_score = -findMoveNegaMaxAlphaBeta(game_state, game_state.getValidMoves(), depth - 1 - 2, -beta, -beta + 1, -turn_multiplier, False)
        game_state.white_to_move = not game_state.white_to_move  # Undo null move
        if null_score >= beta:
            return beta  # Beta cutoff

    # Move Ordering: Sort moves based on their heuristic scores
    valid_moves = orderMoves(game_state, valid_moves)

    max_score = -CHECKMATE
    for move in valid_moves:
        game_state.makeMove(move)
        next_moves = game_state.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        game_state.undoMove()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score


def scoreBoard(game_state):
    """
    Score the board. A positive score is good for white, a negative score is good for black.
    """
    if game_state.checkmate:
        if game_state.white_to_move:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins
    elif game_state.stalemate:
        return STALEMATE
    score = 0
    for row in range(len(game_state.board)):
        for col in range(len(game_state.board[row])):
            piece = game_state.board[row][col]
            if piece != "--":
                piece_position_score = 0
                if piece[1] != "K":
                    piece_position_score = piece_position_scores[piece][row][col]
                if piece[0] == "w":
                    score += piece_score[piece[1]] + piece_position_score
                if piece[0] == "b":
                    score -= piece_score[piece[1]] + piece_position_score

    return score


def findRandomMove(valid_moves):
    """
    Picks and returns a random valid move.
    """
    return random.choice(valid_moves)


def orderMoves(game_state, valid_moves):
    """
    Orders moves based on a heuristic score.
    Prioritizes captures, checks, and promotions.
    """
    def scoreMove(move):
        # Assign a high score for captures (e.g., capturing a queen is better than a pawn)
        if move.piece_captured != "--":
            return piece_score[move.piece_captured[1]] - piece_score[move.piece_moved[1]]
        # Assign a score for checks
        game_state.makeMove(move)
        is_check = game_state.inCheck()
        game_state.undoMove()
        if is_check:
            return 10  # Arbitrary score for checks
        # Assign a score for promotions
        if move.is_pawn_promotion:
            return 8  # Arbitrary score for promotions
        return 0  # Default score for non-special moves

    # Sort moves by their scores in descending order
    return sorted(valid_moves, key=scoreMove, reverse=True)
