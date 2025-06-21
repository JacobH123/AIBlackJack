import numpy as np
import random

def hand_value_np(hand):
    hand = np.array(hand)
    values = np.minimum(hand, 10)
    total = np.sum(values)
    aces = np.count_nonzero(hand == 1)
    while aces > 0 and total + 10 <= 21:
        total += 10
        aces -= 1
    return total


def simulate_game_np(player_hand, dealer_card, deck, move):
    player_hand = player_hand.copy()
    dealer_hand = np.array([dealer_card])
    deck = deck.copy()

    if move == 'hit':
        card = random.choice(deck)
        deck.remove(card)
        player_hand.append(card)
        if hand_value_np(player_hand) > 21:
            return -1

    while hand_value_np(dealer_hand) < 17:
        card = random.choice(deck)
        deck.remove(card)
        dealer_hand = np.append(dealer_hand, card)

    p_score = hand_value_np(player_hand)
    d_score = hand_value_np(dealer_hand)

    if d_score > 21 or p_score > d_score:
        return 1
    elif p_score == d_score:
        return 0
    else:
        return -1


def monte_carlo_eval_np(player_hand, dealer_card, deck, move, num_simulations=5000):
    results = [simulate_game_np(player_hand, dealer_card, deck.copy(), move)
               for _ in range(num_simulations)]
    return np.mean(results)


def recommend_best_move_np(player_hand, dealer_card, deck, num_simulations=5000):
    moves = ['stand', 'hit']
    evs = {move: monte_carlo_eval_np(player_hand, dealer_card, deck, move, num_simulations)
           for move in moves}
    return max(evs, key=evs.get), evs