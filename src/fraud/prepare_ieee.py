import os
import pandas as pd

RAW_DIR = "data/raw/ieee"
OUT_DIR = "data/processed"

def read_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path, low_memory=False)

def merge_tx_id(tx: pd.DataFrame, ident: pd.DataFrame) -> pd.DataFrame:
    return tx.merge(ident, on="TransactionID", how="left")

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    train_tx = read_csv(os.path.join(RAW_DIR, "train_transaction.csv"))
    train_id = read_csv(os.path.join(RAW_DIR, "train_identity.csv"))
    test_tx  = read_csv(os.path.join(RAW_DIR, "test_transaction.csv"))
    test_id  = read_csv(os.path.join(RAW_DIR, "test_identity.csv"))

    train = merge_tx_id(train_tx, train_id)
    test  = merge_tx_id(test_tx, test_id)

    # sanity checks
    assert "isFraud" in train.columns, "isFraud not found in train"
    assert "TransactionDT" in train.columns, "TransactionDT not found in train"
    assert "TransactionID" in train.columns, "TransactionID not found in train"

    train.to_parquet(os.path.join(OUT_DIR, "train.parquet"), index=False)
    test.to_parquet(os.path.join(OUT_DIR, "test.parquet"), index=False)

    print("Saved:")
    print(" - data/processed/train.parquet")
    print(" - data/processed/test.parquet")
    print(f"Train shape: {train.shape}, Test shape: {test.shape}")

if __name__ == "__main__":
    main()