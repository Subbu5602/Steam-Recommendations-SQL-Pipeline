

import os
import sqlite3

import pandas as pd


def load_recommendations(chunk_size=500_000, sample_fraction=0.02, random_state=0):
    chunks = []
    for chunk in pd.read_csv("data/recommendations.csv", chunksize=chunk_size):
        sampled = chunk.sample(frac=sample_fraction, random_state=random_state)
        chunks.append(sampled)
    return pd.concat(chunks, ignore_index=True)


def load_users(chunk_size=500_000, sample_fraction=0.025, random_state=0):
    chunks = []
    for chunk in pd.read_csv("data/users.csv", chunksize=chunk_size):
        sampled = chunk.sample(frac=sample_fraction, random_state=random_state)
        chunks.append(sampled)
    return pd.concat(chunks, ignore_index=True)


def load_games():
    return pd.read_csv("data/games.csv")


def build_database(db_path="steam.db"):
    print("Sampling recommendations.csv...")
    recommendations_df = load_recommendations()
    print(f"  -> {len(recommendations_df)} rows")

    print("Sampling users.csv...")
    users_df = load_users()
    print(f"  -> {len(users_df)} rows")

    print("Loading games.csv...")
    games_df = load_games()
    print(f"  -> {len(games_df)} rows")

    connection = sqlite3.connect(db_path)
    connection.execute("DROP TABLE IF EXISTS recommendations")
    connection.execute("DROP TABLE IF EXISTS users")
    connection.execute("DROP TABLE IF EXISTS games")
    connection.commit()

    recommendations_df.to_sql("Recommendations", connection, if_exists="replace", index=False)
    users_df.to_sql("Users", connection, if_exists="replace", index=False)
    games_df.to_sql("Games", connection, if_exists="replace", index=False)

    size_mb = os.path.getsize(db_path) / (1024 * 1024)
    print(f"Done. {db_path} is {size_mb:.1f} MB")

    connection.close()


if __name__ == "__main__":
    build_database()
