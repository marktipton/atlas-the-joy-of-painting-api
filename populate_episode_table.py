#!/usr/bin/env python3

import pandas as pd
import re

def normalize_title(title):
    # Convert to lowercase
    title = title.lower()
    # replace abbreviations
    title = re.sub(r'\bmt\.?\b', 'mount', title)
    title = re.sub(r'\band\b', '&', title)

    #remove punctuation
    title = re.sub(r'[^\w\s]', '', title)
    return title.strip()

# read episode dates
with open('episode_dates.txt', 'r') as f:
    date_lines = f.readlines()

dates_dict = {}

for line in date_lines:
    date_start = line.rfind('(')
    date_end = line.rfind(')')
    if date_start == -1 or date_end == -1:
        print(f"Skipping line due to incorrect format: {line.strip()}")
        continue

    title = line[:date_start].strip().strip('"')
    date = line[date_start + 1:date_end].strip()

    normalized_title = normalize_title(title)
    dates_dict[normalized_title] = date

# dataFrame for episodes data
df = pd.read_csv('bob_ross_colors.csv')

df['normalized_title'] = df['painting_title'].apply(normalize_title)

# add date to dataframe by matching title
df['date'] = df['normalized_title'].map(dates_dict)


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

df.to_csv('bob_ross_colors_with_dates.csv', index=False)

print("dates matched, split, and saved")
