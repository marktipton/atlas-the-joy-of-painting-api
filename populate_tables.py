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
