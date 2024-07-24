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

for line in dates_lines:
    title, date = line.split(' (')
    date = date.rstrip(')\n')
    normalized_title = normalize_title(title)
    dates_dict[normalized_title] = date

dataFrameEpisodes = pd.read_csv('bob_ross_colors.csv')
