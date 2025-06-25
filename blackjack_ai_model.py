from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import joblib

df = pd.read_csv("blackjack_training_data.csv")
X = df[['player_total', 'has_ace', 'dealer_card', 'num_aces', 'hand_size', 'soft_total', 'bust_risk']]
y = df['move']

model = RandomForestClassifier(max_depth=5)
model.fit(X, y)

joblib.dump(model, "blackjack_ai_model.joblib")
print("Model saved to blackjack_ai_model.joblib")
