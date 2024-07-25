#!/usr/bin/env python3

import pandas as pd
import psycopg2
from psycopg2 import sql

c = psycopg2.connect(
    dbname="joyofcoding",
    user="bob",
    password="ross",
    host="127.0.0.1",
    port="5432"
)

# open cursor to perform operations on database
cursor = c.cursor()

# Create the episodes table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS episodes (
    id SERIAL PRIMARY KEY,
    painting_index INTEGER,
    img_src VARCHAR,
    title VARCHAR,
    season INTEGER,
    episode_number INTEGER,
    youtube_src VARCHAR,
    date DATE,
    month INTEGER,
    day INTEGER,
    year INTEGER,
    note TEXT
);
"""
cursor.execute(create_table_query)

# load data into pandas DataFrames
df_episodes = pd.read_csv('bob_ross_colors_with_dates.csv')
# df_subjects = pd.read_csv('bob_ross_subjects.csv')

# Insert DataFrame records one by one into the episodes table
for index, row in df_episodes.iterrows():
    insert_query = sql.SQL("""
    INSERT INTO episodes (painting_index, img_src, title, season, episode_number, youtube_src, date, month, day, year, note)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """)
    cursor.execute(insert_query, (
        row['painting_index'],
        row['img_src'],
        row['painting_title'],
        row['season'],
        row['episode'],
        row['youtube_src'],
        row['date'],
        row['month'],
        row['day'],
        row['year'],
        row['note']
    ))

# commit changes to db
c.commit()
# close cursor and connection to db
cursor.close()
c.close()
