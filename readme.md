# Aave V2 Wallet Credit Scoring

## 🧠 Objective

Assign a credit score between **0 and 1000** to wallets that interact with the Aave V2 protocol. Scores reflect user behavior — higher = trustworthy, lower = risky.

## 🔍 Features Engineered

From each wallet's transaction history:
- Number of `deposit`, `borrow`, `repay`, `redeemunderlying`, `liquidationcall`
- Total amount of `borrow` and `repay`
- Ratio of repay to borrow
- Liquidation count

## 📊 Scoring Logic

We calculate a **raw score** using:

```python
raw_score = (repay_ratio * 2) - (liquidation_count + 1)
