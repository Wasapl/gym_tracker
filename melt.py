import os
import sqlite3
from datetime import datetime
import re

# Create SQLite database and table
db_name = os.getenv("GYM_DB", "habit_tracker.db")
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS reshaped_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    heading TEXT,
    date TEXT,
    exercise TEXT,
    value TEXT
)
''')
conn.commit()

# Step 2: Read data from original table
cursor.execute('SELECT filename, heading, date, bench_press, bench_press_2, bench_press_3, pull_down, seated_row, triceps, Bulgarian_Squat, Leg_extension, Leg_curl, Leg_press, Calf_extension, fitband_duration, fitband_kcal, fitband_heartrate, full_text, row_machine, inc_bells_press, lat_rises FROM habit_data')
rows = cursor.fetchall()

# Step 3: Insert reshaped rows into the new table
reshaped_rows = []
for row in rows:
    filename, heading, date, bench_press, bench_press_2, bench_press_3, pull_down, seated_row, triceps, Bulgarian_Squat, Leg_extension, Leg_curl, Leg_press, Calf_extension, fitband_duration, fitband_kcal, fitband_heartrate, full_text, row_machine, inc_bells_press, lat_rises = row
    match = re.search(r'(?<= - ).*?(?= \w+\.md)', filename)
    if match:
        conditions = match.group(0)
    else:
        conditions = None  # Default to None if no date found
    if "мельдоний" in filename:
        meldoniy = "yes"
    else:
        meldoniy = None

    reshaped_rows.extend([
        (filename, heading, date, 'bench_press', bench_press),
        (filename, heading, date, 'bench_press_2', bench_press_2),
        (filename, heading, date, 'bench_press_3', bench_press_3),
        (filename, heading, date, 'pull_down', pull_down),
        (filename, heading, date, 'seated_row', seated_row),
        (filename, heading, date, 'triceps', triceps),
        (filename, heading, date, 'Bulgarian_Squat', Bulgarian_Squat),
        (filename, heading, date, 'Leg_extension', Leg_extension),
        (filename, heading, date, 'Leg_curl', Leg_curl),
        (filename, heading, date, 'Leg_press', Leg_press),
        (filename, heading, date, 'Calf_extension', Calf_extension),
        (filename, heading, date, 'fitband_duration', fitband_duration),
        (filename, heading, date, 'fitband_kcal', fitband_kcal),
        (filename, heading, date, 'fitband_heartrate', fitband_heartrate),
        (filename, heading, date, 'full_text', full_text),
        (filename, heading, date, 'row_machine', row_machine),
        (filename, heading, date, 'inc_bells_press', inc_bells_press),
        (filename, heading, date, 'lat_rises', lat_rises),
        (filename, heading, date, 'meldoniy', meldoniy),
        (filename, heading, date, 'conditions', conditions),
    ])

# cursor.executemany('INSERT INTO reshaped_data (filename, heading, date, exercise, value) VALUES (?, ?, ?, ?, ?)', reshaped_rows)

# Commit and close
conn.commit()

conn.close()

print("Data reshaped and inserted into 'reshaped_data' table.")