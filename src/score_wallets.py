import json
import pandas as pd
from collections import defaultdict
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# Load JSON
with open("data/user_transactions.json", "r") as f:
    data = json.load(f)

wallet_data = defaultdict(lambda: defaultdict(float))
wallet_tx_count = defaultdict(int)

# Feature Extraction
for tx in data:
    wallet = tx["user"]
    action = tx["action"].lower()
    amount = float(tx.get("amount", 0))

    wallet_tx_count[wallet] += 1
    wallet_data[wallet][f"count_{action}"] += 1
    wallet_data[wallet][f"sum_{action}"] += amount

wallet_df = pd.DataFrame.from_dict(wallet_data, orient='index')
wallet_df["tx_count"] = wallet_df.index.map(wallet_tx_count)
wallet_df.fillna(0, inplace=True)

# Score Calculation
wallet_df["repay_ratio"] = wallet_df["sum_repay"] / (wallet_df["sum_borrow"] + 1)
wallet_df["risk"] = wallet_df["count_liquidationcall"] + 1
wallet_df["raw_score"] = (wallet_df["repay_ratio"] * 2) - (wallet_df["risk"])

# Normalize score to 0–1000
scaler = MinMaxScaler(feature_range=(0, 1000))
wallet_df["credit_score"] = scaler.fit_transform(wallet_df[["raw_score"]])

# Save score
wallet_df[["credit_score"]].to_csv("wallet_scores.csv")

# Plot distribution
bins = list(range(0, 1100, 100))
plt.figure(figsize=(10, 6))
plt.hist(wallet_df["credit_score"], bins=bins, edgecolor="black")
plt.title("Credit Score Distribution")
plt.xlabel("Score Range")
plt.ylabel("Number of Wallets")
plt.savefig("score_distribution.png")
print("✅ Scoring complete. Files saved.")
