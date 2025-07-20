import json
import pandas as pd
from collections import defaultdict
from tqdm import tqdm

# Load the raw transaction JSON file
def load_data(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data)

# Save final scores to a CSV file
def save_scores(scores_dict, output_path="wallet_scores.csv"):
    df = pd.DataFrame(scores_dict.items(), columns=["wallet", "score"])
    df.to_csv(output_path, index=False)
    print(f"✅ Scores saved to {output_path}")

# Extract useful features from the data per wallet
def extract_features(df):
    wallet_features = defaultdict(lambda: {
        "deposits": 0,
        "borrows": 0,
        "repays": 0,
        "redeems": 0,
        "liquidations": 0,
        "unique_assets": set(),
        "timestamps": []
    })

    # Normalize action types
    action_map = {
        "deposit": "deposits",
        "borrow": "borrows",
        "repay": "repays",
        "redeemunderlying": "redeems",
        "liquidationcall": "liquidations"
    }

    for _, row in tqdm(df.iterrows(), total=len(df), desc="🔍 Processing transactions"):
        wallet = row.get("userWallet", "unknown").lower()
        action = row.get("action", "").lower()
        token = row.get("actionData", {}).get("assetSymbol", "")
        timestamp = row.get("timestamp", 0)

        if action in action_map:
            wallet_features[wallet][action_map[action]] += 1

        if token:
            wallet_features[wallet]["unique_assets"].add(token)
        if timestamp:
            wallet_features[wallet]["timestamps"].append(timestamp)

    # Finalize features
    final_features = {}
    for wallet, feats in wallet_features.items():
        txns = feats["timestamps"]
        txns.sort()
        avg_gap = (txns[-1] - txns[0]) / len(txns) if len(txns) > 1 else 0
        final_features[wallet] = {
            "deposits": feats["deposits"],
            "borrows": feats["borrows"],
            "repays": feats["repays"],
            "redeems": feats["redeems"],
            "liquidations": feats["liquidations"],
            "asset_count": len(feats["unique_assets"]),
            "txn_count": len(txns),
            "avg_time_gap": avg_gap
        }

    return pd.DataFrame.from_dict(final_features, orient="index")

# Assign credit scores to wallets based on engineered features
def calculate_scores(features_df):
    scores = {}
    for wallet, row in features_df.iterrows():
        score = 600  # Base score

        # Positive behavior
        score += row["repays"] * 15
        score += row["deposits"] * 10
        score += row["asset_count"] * 5

        # Negative behavior
        score -= row["liquidations"] * 50
        score -= row["borrows"] * 5

        # Inactivity penalty
        if row["txn_count"] < 3:
            score -= 100

        # Clamp score between 0 and 1000
        score = max(0, min(1000, int(score)))
        scores[wallet] = score

    return scores

# Main runner
def main():
    path = "data/user_transactions.json"  # Make sure this is the correct path
    print("📥 Loading data...")
    df = load_data(path)

    print("🛠️ Extracting features...")
    features = extract_features(df)

    print("🧮 Calculating scores...")
    scores = calculate_scores(features)

    print("💾 Saving scores...")
    save_scores(scores)

if __name__ == "__main__":
    main()
