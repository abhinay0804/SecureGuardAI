#!/usr/bin/env python3
"""Seed MongoDB with CSV files from data/processed.

Usage:
  python seed_db.py --dir ../data/processed
"""
import argparse
import os
import sys
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, ROOT)

from src.utils.fraud_dashboard.database import get_collection


def seed_transactions(csv_path, collection):
    df = pd.read_csv(csv_path)
    # Convert NaNs to None for Mongo insertion
    records = df.where(pd.notnull(df), None).to_dict(orient="records")
    if not records:
        print(f"No records found in {csv_path}")
        return 0
    try:
        res = collection.insert_many(records)
        print(f"Inserted {len(res.inserted_ids)} records from {csv_path}")
        return len(res.inserted_ids)
    except Exception as e:
        print("Error inserting records:", e)
        return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default="../data/processed", help="Directory with CSVs")
    args = parser.parse_args()

    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), args.dir))
    if not os.path.isdir(data_dir):
        print("Data directory not found:", data_dir)
        return

    coll = get_collection("transactions")
    if coll is None:
        print("No database available (using MockCollection). Seeding skipped.")
        return

    total = 0
    for fname in os.listdir(data_dir):
        if fname.endswith('.csv'):
            path = os.path.join(data_dir, fname)
            total += seed_transactions(path, coll)

    print(f"Seeding complete. Total inserted: {total}")


if __name__ == "__main__":
    main()
