import joblib
import pandas as pd
from blackJack_AI import hand_value_np

model = joblib.load("blackjack_ai_model.joblib")

def recommend_best_move_model(player_hand, dealer_card):
    features = pd.DataFrame([{
        'player_total': hand_value_np(player_hand),
        'has_ace': 1 if 1 in player_hand else 0,
        'dealer_card': dealer_card,
        'num_aces': player_hand.count(1),
        'hand_size': len(player_hand),
        'soft_total': 1 if (1 in player_hand and hand_value_np(player_hand) <= 21 and hand_value_np(player_hand) - sum(min(card, 10) for card in player_hand) >= 10) else 0,
        'bust_risk': 1 if 12 <= hand_value_np(player_hand) <= 16 else 0
    }])

    probs = model.predict_proba(features)[0]
    move = 'hit' if probs[1] > probs[0] else 'stand'
    
    return move, {'hit': probs[1], 'stand': probs[0]}
