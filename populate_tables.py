#!/usr/bin/env python3

import pandas as pd
import psycopg2
from psycopg2 import sql
from combine_dates_and_colors import normalize_title

c = psycopg2.connect(
    dbname="joyofcoding",
    user="bob",
    password="ross",
    host="127.0.0.1",
    port="5432"
)

# open cursor to perform operations on database
cursor = c.cursor()

create_episode_table = """
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
cursor.execute(create_episode_table)

create_colors_table = """
CREATE TABLE IF NOT EXISTS colors (
    id SERIAL PRIMARY KEY,
    color_name VARCHAR UNIQUE,
    hex_code VARCHAR
);
"""

cursor.execute(create_colors_table)

create_episodes_colors_table = """
CREATE TABLE IF NOT EXISTS episodes_colors (
    id SERIAL PRIMARY KEY,
    episode_id INTEGER REFERENCES episodes(id),
    color_id INTEGER REFERENCES colors(id)
);
"""
cursor.execute(create_episodes_colors_table)

# Create the subjects table if it doesn't exist
create_subjects_table = """
CREATE TABLE IF NOT EXISTS subjects (
    id SERIAL PRIMARY KEY,
    subject_name VARCHAR UNIQUE
);
"""
cursor.execute(create_subjects_table)

# Create the episodes_subjects table if it doesn't exist
create_episodes_subjects_table = """
CREATE TABLE IF NOT EXISTS episodes_subjects (
    id SERIAL PRIMARY KEY,
    episode_id INTEGER REFERENCES episodes(id),
    subject_id INTEGER REFERENCES subjects(id)
);
"""
cursor.execute(create_episodes_subjects_table)

# load data into pandas DataFrames
df_episodes = pd.read_csv('bob_ross_colors_with_dates.csv')
df_subjects = pd.read_csv('bob_ross_subjects.csv')
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

# colors and corresponding hex codes
colors_and_hex = {
    'Black_Gesso': '#000000',
    'Bright_Red': '#DB0000',
    'Burnt_Umber': '#8A3324',
    'Cadmium_Yellow': '#FFEC00',
    'Dark_Sienna': '#3C1414',
    'Indian_Red': '#CD5C5C',
    'Indian_Yellow': '#E3A857',
    'Liquid_Black': '#000000',
    'Liquid_Clear': '#FFFFFF',
    'Midnight_Black': '#343434',
    'Phthalo_Blue': '#000F89',
    'Phthalo_Green': '#102E3C',
    'Prussian_Blue': '#021E44',
    'Sap_Green': '#0A3410',
    'Titanium_White': '#FFFFFF',
    'Van_Dyke_Brown': '#221B15',
    'Yellow_Ochre': '#CB823B',
    'Alizarin_Crimson': '#4E1500'
}

# Insert unique colors and hex codes into the colors table
for color_name, hex_code in colors_and_hex.items():
    cursor.execute("""
    INSERT INTO colors (color_name, hex_code)
    VALUES (%s, %s)
    ON CONFLICT (color_name) DO NOTHING
    """, (color_name, hex_code))

# Insert data into the episodes_colors junction table
for index, row in df_episodes.iterrows():
    # Get the episode id
    cursor.execute("SELECT id FROM episodes WHERE painting_index = %s", (row['painting_index'],))
    episode_id = cursor.fetchone()[0]

    for color_name in colors_and_hex.keys():
        if row[color_name] == 1:
            cursor.execute("SELECT id FROM colors WHERE color_name = %s", (color_name,))
            color_id = cursor.fetchone()[0]
            cursor.execute("""
            INSERT INTO episodes_colors (episode_id, color_id)
            VALUES (%s, %s)
            """, (episode_id, color_id))

# Dynamically generate subjects list from the DataFrame column headers
subjects_list = [col for col in df_subjects.columns if col not in ['EPISODE', 'TITLE']]

# Insert unique subjects into the subjects table
for subject in subjects_list:
    cursor.execute("""
    INSERT INTO subjects (subject_name)
    VALUES (%s)
    ON CONFLICT (subject_name) DO NOTHING
    """, (subject,))

# commit changes to db
c.commit()
# close cursor and connection to db
cursor.close()
c.close()
