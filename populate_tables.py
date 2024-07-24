#!/usr/bin/env python3

import pandas as pd
import psycopg2

c = psycopg2.connect(
    dbname="joyofcoding",
    user="bob",
    password="ross",
    host="127.0.0.1",
    port="5432"
)

# open cursor to perform operations on database
cursor = c.cursor()

# load data into pandas DataFrames
df_colors = pd.read_csv('bob_ross_colors.csv')
df_subjects = pd.read_csv('bob_ross_subjects.csv')

# commit changes to db
c.commit()
# close cursor and connection to db
cursor.close()
c.close()
