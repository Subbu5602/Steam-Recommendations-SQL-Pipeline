

import os
import sqlite3

import pandas as pd


def load_recommendations(chunk_size=500_000, sample_fraction=0.02, random_state=0):
    chunks = []
    for chunk in pd.read_csv("data/recommendations.csv", chunksize=chunk_size):
        sampled = chunk.sample(frac=sample_fraction, random_state=random_state)
        chunks.append(sampled)
    recommendations_df = pd.concat(chunks,ignore_index=True)
    unique_ids = set(recommendations_df["user_id"].unique())
    return recommendations_df, unique_ids


def load_users(unique_ids, chunk_size=500_000):
    chunks = []
    for chunk in pd.read_csv("data/users.csv", chunksize=chunk_size):
        sampled = chunk[chunk["user_id"].isin(unique_ids)]
        chunks.append(sampled)
    return pd.concat(chunks, ignore_index=True)


def load_games():
    return pd.read_csv("data/games.csv")


def build_database(db_path="steam.db"):
    print("Sampling recommendations.csv...")
    recommendations_df,unique_ids = load_recommendations()
    print(f"  -> {len(recommendations_df)} rows")

    print("Filtering users.csv...")
    users_df = load_users(unique_ids)
    print(f"  -> {len(users_df)} rows")

    print("Loading games.csv...")
    games_df = load_games()
    print(f"  -> {len(games_df)} rows")

    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys=ON")
    connection.execute("DROP TABLE IF EXISTS recommendations")
    connection.execute("DROP TABLE IF EXISTS users")
    connection.execute("DROP TABLE IF EXISTS games")
    connection.execute("Create table Users(user_id INTEGER NOT NULL PRIMARY KEY, products INTEGER NOT NULL, reviews INTEGER NOT NULL)")

    connection.execute("Create table Games(app_id INTEGER NOT NULL PRIMARY KEY, title VARCHAR(200) NOT NULL, date_release DATE NOT NULL, win BOOLEAN NOT NULL, mac BOOLEAN NOT NULL, linux BOOLEAN NOT NULL, rating VARCHAR(100) NOT NULL, positive_ratio INTEGER NOT NULL, user_reviews INTEGER NOT NULL, price_final DOUBLE NOT NULL, price_original DOUBLE NOT NULL, discount DOUBLE NOT NULL, steam_deck BOOLEAN NOT NULL)")


    connection.execute("Create table Recommendations (app_id INTEGER NOT NULL, helpful INTEGER NOT NULL, funny INTEGER NOT NULL, date DATE NOT NULL, is_recommended BOOLEAN NOT NULL, hours DOUBLE NOT NULL, user_id INTEGER NOT NULL, review_id INTEGER NOT NULL PRIMARY KEY, CONSTRAINT fk_Users FOREIGN KEY (user_id) REFERENCES Users(user_id), CONSTRAINT fk_Games FOREIGN KEY(app_id) REFERENCES Games(app_id))")

    
    connection.commit()

    users_df.to_sql("Users", connection, if_exists="append", index=False)
    games_df.to_sql("Games", connection, if_exists="append", index=False)
    recommendations_df.to_sql("Recommendations", connection, if_exists="append", index=False)
    

    size_mb = os.path.getsize(db_path) / (1024 * 1024)
    print(f"Done. {db_path} is {size_mb:.1f} MB")

    connection.close()


if __name__ == "__main__":
    build_database()
