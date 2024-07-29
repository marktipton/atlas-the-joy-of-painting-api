#!/usr/bin/env python3

import pandas as pd
from normalize_data import normalize_title

# Load the combined data with subjects
df_combined = pd.read_csv('bob_ross_colors_with_dates.csv')

# Load the subjects data
df_subjects = pd.read_csv('bob_ross_subjects.csv')

# Normalize titles in the subjects DataFrame
df_subjects['normalized_title'] = df_subjects['TITLE'].apply(normalize_title)

# Convert presence to numeric, errors='coerce' will turn non-numeric entries to NaN
df_subjects = df_subjects.apply(pd.to_numeric, errors='ignore')

# Create a long-format DataFrame for subjects data
df_subjects_long = df_subjects.melt(id_vars=['normalized_title'], var_name='subject', value_name='presence')

# Ensure 'presence' is numeric (convert errors to NaN and then fill NaNs with 0)
df_subjects_long['presence'] = pd.to_numeric(df_subjects_long['presence'], errors='coerce').fillna(0).astype(int)

# Pivot the long-format DataFrame to wide format
df_subjects_wide = df_subjects_long.pivot_table(index='normalized_title', columns='subject', values='presence', fill_value=0)

# Reset index to have normalized_title as a column
df_subjects_wide.reset_index(inplace=True)

# Normalize titles in the combined DataFrame
df_combined['normalized_title'] = df_combined['painting_title'].apply(normalize_title)

# Merge the wide-format subjects DataFrame with the combined DataFrame
df_combined = df_combined.merge(df_subjects_wide, left_on='normalized_title', right_on='normalized_title', how='left')

# Drop the intermediate normalized title column
df_combined.drop(columns=['normalized_title'], inplace=True)

# Save the updated DataFrame with subjects as columns
df_combined.to_csv('bob_ross_colors_with_dates_and_subjects.csv', index=False)

print("Subjects have been added as columns, and the data has been saved.")