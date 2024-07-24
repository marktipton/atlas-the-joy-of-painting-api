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


