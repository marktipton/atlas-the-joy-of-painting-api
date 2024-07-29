#!/usr/bin/env python3

import pandas as pd
import re
from fuzzywuzzy import process
from normalize_data import normalize_title

# read episode dates
with open('episode_dates.txt', 'r') as f:
    date_lines = f.readlines()

dates_dict = {}
notes_dict = {}

for line in date_lines:
    date_start = line.find('(')
    date_end = line.find(')')
    if date_start == -1 or date_end == -1:
        print(f"Skipping line due to incorrect format: {line.strip()}")
        continue

    title = line[:date_start].strip().strip('"')
    date = line[date_start + 1:date_end].strip()

    note_start = date_end + 1
    note = line[note_start:].strip()
    # Check if there are additional parentheses in the note
    if '(' in note and ')' in note:
        note_start = note.find('(')
        note_end = note.find(')', note_start + 1)
        if note_start != -1 and note_end != -1:
            additional_note = note[note_start:note_end+1]
            note = note[:note_start].strip() + ' ' + additional_note

    normalized_title = normalize_title(title)
    # print(normalized_title)
    dates_dict[normalized_title] = date
    notes_dict[normalized_title] = note if note else None

# dataFrame for episodes data
df = pd.read_csv('bob_ross_colors.csv')

df['normalized_title'] = df['painting_title'].apply(normalize_title)

# DataFrame for subjects data
df_subjects = pd.read_csv('bob_ross_subjects.csv')
df_subjects['normalized_title'] = df_subjects['TITLE'].apply(normalize_title)

# find closest title
def get_date_from_closest_title(title):
    match, score = process.extractOne(title, dates_dict.keys())
    if score > 70:
        return dates_dict[match]
    return None

# add date to episodes dataframe by matching title
df['date'] = df['normalized_title'].apply(get_date_from_closest_title)

# convert date column to datetime object
df['date'] = pd.to_datetime(df['date'], errors='coerce', format='%B %d, %Y')

# separate date into month day year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['year'] = df['date'].dt.year

# add note if it is there
df['note'] = df['normalized_title'].map(notes_dict)

# Remove decimal points from month, day, and year columns
df['month'] = df['month'].astype(int)
df['day'] = df['day'].astype(int)
df['year'] = df['year'].astype(int)

df.drop(columns=['normalized_title'], inplace=True)

df.to_csv('bob_ross_colors_with_dates.csv', index=False)

# Convert the subjects DataFrame to long format for merging
df_subjects_long = df_subjects.melt(id_vars=['normalized_title'], var_name='subject', value_name='presence')

# Debugging: Print column names to verify
print("df columns:", df.columns)
print("df_subjects_long columns:", df_subjects_long.columns)

# Add subject presence/absence data by merging
df_episodes_subjects = df.merge(df_subjects_long, left_on='normalized_title', right_on='normalized_title', how='left')

# Drop intermediate columns and rename columns
df_episodes_subjects.rename(columns={
    'painting_title': 'episode_title',
    'subject': 'subject_name',
    'presence': 'subject_presence'
}, inplace=True)

# Drop 'normalized_title' column if it exists
df_episodes_subjects.drop(columns=['normalized_title'], inplace=True, errors='ignore')

# Save the updated DataFrame with presence/absence data
df_episodes_subjects.to_csv('bob_ross_colors_with_dates_and_subjects.csv', index=False)
print("dates matched, split, and saved")
