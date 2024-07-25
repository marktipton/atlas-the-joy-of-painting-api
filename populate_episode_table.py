#!/usr/bin/env python3

import pandas as pd
import re
from fuzzywuzzy import process

def normalize_title(title):
    # Convert to lowercase
    title = title.lower()
    # replace abbreviations
    title = re.sub(r'\bmt\.?\b', 'mount', title)
    title = re.sub(r'\band\b', '&', title)
    # remove punctuation
    title = re.sub(r'[^\w\s]', '', title)
    # remove spaces
    title = re.sub(r'\s+', '', title)
    # remove trailing 's' only if preceded by a space
    title = re.sub(r'(\S)s$', r'\1', title)
    return title

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
    print(normalized_title)
    dates_dict[normalized_title] = date
    notes_dict[normalized_title] = note if note else None

# dataFrame for episodes data
df = pd.read_csv('bob_ross_colors.csv')

df['normalized_title'] = df['painting_title'].apply(normalize_title)

# find closest title
def get_date_from_closest_title(title):
    match, score = process.extractOne(title, dates_dict.keys())
    if score > 70:
        return dates_dict[match]
    return None

# add date to dataframe by matching title
df['date'] = df['normalized_title'].apply(get_date_from_closest_title)
df['note'] = df['normalized_title'].map(notes_dict)

# convert date column to datetime object
df['date'] = pd.to_datetime(df['date'], errors='coerce', format='%B %d, %Y')

# Check for any rows where date conversion failed
print(df[df['date'].isna()])

# separate date into month day year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['year'] = df['date'].dt.year

# Remove decimal points from month, day, and year columns
df['month'] = df['month'].astype(int)
df['day'] = df['day'].astype(int)
df['year'] = df['year'].astype(int)

df.drop(columns=['normalized_title'], inplace=True)

# df.to_csv('bob_ross_colors_with_dates.csv', index=False)

print("dates matched, split, and saved")
