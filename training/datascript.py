import sys
import os
import numpy as np
# Add the parent directory of this script to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import random
from blackJack_AI import hand_value_np, recommend_best_move_np 

data = []

for _ in range(50000):  
    full_deck = [1,2,3,4,5,6,7,8,9,10,10,10,10] * 4
    random.shuffle(full_deck)

    player_hand = [full_deck.pop(), full_deck.pop()]
    dealer_card = full_deck.pop()
    deck = full_deck.copy()
    player_total = hand_value_np(player_hand)
    has_ace = 1 if 1 in player_hand else 0
    num_aces = player_hand.count(1)
    hand_size = len(player_hand)
    soft_total = 1 if (1 in player_hand and player_total <= 21 and player_total - np.sum(np.minimum(player_hand, 10)) >= 10) else 0
    dealer_card_val = dealer_card
    bust_risk = 1 if 12 <= player_total <= 16 else 0  #high-risk flag


    # Use Monte Carlo 
    best_move, _ = recommend_best_move_np(player_hand, dealer_card, deck, num_simulations=100)

    data.append({
        'player_total': player_total,
        'has_ace': has_ace,
        'num_aces': num_aces,
        'hand_size': hand_size,
        'soft_total': soft_total,
        'dealer_card': dealer_card_val,
        'bust_risk': bust_risk,
        'move': 1 if best_move == 'hit' else 0
    })
df = pd.DataFrame(data)
df.to_csv("blackjack_training_data.csv", index=False)
print("Training data saved to blackjack_training_data.csv")
