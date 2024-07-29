#!/usr/bin/env python3

import re

def normalize_title(title):
    # Convert to lowercase
    title = title.lower()
    # replace abbreviations
    title = re.sub(r'\bmt\.?\b', 'mount', title)
    title = re.sub(r'\band\b', '&', title)
    # remove punctuation
    title = re.sub(r'[^\w\s]', '', title)
    # split and order words to handle names that are in different orders
    words = title.split()
    words.sort()
    normalized_title = ' '.join(words)

    return normalized_title