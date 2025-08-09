import os
import sqlite3
from datetime import datetime
import re


# Create SQLite database and table
db_name = os.getenv("GYM_DB", "habit_tracker.db")
conn = sqlite3.connect(db_name)
cursor = conn.cursor()


# count the number of rows in the reshaped_data table
cursor.execute('SELECT COUNT(*) FROM reshaped_data')
count = cursor.fetchone()[0]
print(f"Total rows inserted into reshaped_data: {count}")

# count the number of unique dates in the reshaped_data table
cursor.execute('SELECT COUNT(DISTINCT date) FROM reshaped_data')
unique_dates_count = cursor.fetchone()[0]
print(f"Total unique dates in reshaped_data: {unique_dates_count}")

# print max and min dates in the reshaped_data table
cursor.execute('SELECT MAX(date), MIN(date) FROM reshaped_data')
max_date, min_date = cursor.fetchone()
print(f"Max date in reshaped_data: {max_date}")
print(f"Min date in reshaped_data: {min_date}")

# print all duplicate rows for date+exercise
cursor.execute('''SELECT date, exercise, COUNT(*) as count
FROM reshaped_data
GROUP BY date, exercise
HAVING count > 1''')
duplicates = cursor.fetchall()
if duplicates:
    print("Duplicate rows found for date+exercise:")
    for dup in duplicates:
        print(dup)

conn.close()
