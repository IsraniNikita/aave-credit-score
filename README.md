# Credit Scoring Model for Aave V2 Wallets

## 📌 Project Overview

This project builds a credit scoring model for wallets interacting with the Aave V2 protocol on the Polygon network. The goal is to evaluate the financial behavior of each wallet based on historical transaction activity and assign a credit score between 0 and 1000, where a higher score indicates a more trustworthy borrower.

## 🧩 Dataset

Format: JSON (30k+ entries)

Each entry includes:

userWallet: wallet address

action: type of activity (e.g., deposit, borrow, repay)

actionData: details like amount, asset type, etc.

timestamp: time of transaction

Sample actions observed:

deposit, borrow, repay, redeemUnderlying, liquidationCall

## 🛠️ Feature Engineering

For each wallet, we extract these features:

Feature

Description

deposits

Number of deposits made

borrows

Number of borrows

repays

Number of times debt was repaid

redeems

Number of redeems (withdrawals)

liquidations

Times the wallet was liquidated

asset_count

Number of unique tokens interacted with

txn_count

Total number of interactions

avg_time_gap

Average time gap between transactions

## 📈 Scoring Logic

- We assign a base score of 600 and then:

## 🔼 Add for Positive Behavior:

- +15 for each repay

- +10 for each deposit

- +5 per unique asset interacted with

## 🔽 Subtract for Negative Behavior:

- -50 for each liquidation

- -5 for each borrow

- -100 if the wallet had <3 total transactions

- Scores are clamped between 0 and 1000.

## 💾 Output

- Output is saved to wallet_scores.csv with the format:

wallet,score
0xabc123...,735
0xdef456...,620

## 📂 Files

- score_wallets.py: main script

- data/user_transactions.json: input data

- wallet_scores.csv: final output

## 🚀 How to Run

- python score_wallets.py

- Make sure your terminal is inside the project folder and your JSON file is in the correct path (data/).

## ✅ Notes

- Handles missing or malformed data gracefully

- Progress bar using tqdm

- Efficient processing for large datasets


