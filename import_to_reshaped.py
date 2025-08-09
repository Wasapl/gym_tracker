import logging
import os
import sqlite3
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create SQLite database and table
db_name = os.getenv("GYM_DB", "habit_tracker.db")
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

def convert_date_to_iso(date_str):
    """Convert date string from 'MM/DD/YYYY' to 'YYYY-MM-DD' format."""
    try:
        return datetime.strptime(date_str, "%m/%d/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return None  # Return None if the date format is invalid

# Function to extract required data from a file
def extract_data_from_file(filepath, cursor):
    reshaped_rows = []
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        filename = os.path.basename(filepath)

    heading = lines[0].strip("# ").strip() if lines else None
    date_line = next((line for line in lines if line.startswith("Date:")), None)
    if date_line:
        raw_date = date_line.split(":", 1)[1].strip()
        date = convert_date_to_iso(raw_date)
    else:
        date = None

    full_text = "".join([line for line in lines if line.strip()])
    reshaped_rows.extend([(filename, heading, date, 'full_text', full_text)])

    for line in lines:
        line = line.lower().replace("**", "").strip()
        if line.startswith("+жим от груди") and \
                not line.startswith("+жим от груди 2") and \
                not line.startswith("+жим от груди 3"):
            reshaped_rows.extend([(filename, heading, date, 'bench_press', line.replace("+жим от груди ", "").strip())])
        elif line.startswith("+жим от груди 2"):
            reshaped_rows.extend([(filename, heading, date, 'bench_press_2', line.replace("+жим от груди ", "").strip())])
        elif line.startswith("+жим от груди 3"):
            reshaped_rows.extend([(filename, heading, date, 'bench_press_3', line.replace("+жим от груди 3поз стула", "").strip())])
        elif line.startswith("+pull down"):
            reshaped_rows.extend([(filename, heading, date, 'pull_down', line.replace("+pull down ", "").strip())])
        elif line.startswith("+seated row"):
            reshaped_rows.extend([(filename, heading, date, 'seated_row', line.replace("+seated row ", "").strip())])
        elif line.startswith("+трицепс "):
            reshaped_rows.extend([(filename, heading, date, 'triceps', line.replace("+трицепс ", "").strip())])
        elif line.startswith("+bulgarian split squat**"):
            reshaped_rows.extend([(filename, heading, date, 'Bulgarian_Squat', line.replace("+bulgarian split squat", "").strip())])
        elif line.startswith("+leg extension") and not line == "leg extension - показалось что болгарские более общие чем это.\n":
            reshaped_rows.extend([(filename, heading, date, 'Leg_extension', line.replace("+leg extension", "").strip())])
        elif line.startswith("+leg curl"):
            reshaped_rows.extend([(filename, heading, date, 'Leg_curl', line.replace("+leg curl", "").strip())])
        elif line.startswith("+leg press"):
            reshaped_rows.extend([(filename, heading, date, 'Leg_press', line.replace("+leg press", "").strip())])
        elif line.startswith("+calf extension"):
            reshaped_rows.extend([(filename, heading, date, 'Calf_extension', line.replace("+calf extension", "").strip())])
        elif line.startswith("duration") and not line.startswith("duration 0:00:00"):
            reshaped_rows.extend([(filename, heading, date, 'fitband_duration', line.split(" ", 1)[1].strip())])
        elif " kcal" in line and not line == "00 kcal\n":
            reshaped_rows.extend([(filename, heading, date, 'fitband_kcal', line.split(" ", 1)[0].strip())])
        elif line.startswith("heart rate") and not line == "heart rate 0 avg, 0 max (aerobic 0min)\n":
            reshaped_rows.extend([(filename, heading, date, 'fitband_heartrate', line.replace("heart rate", "").strip())])
        elif line.startswith("+rowing machine "):
            reshaped_rows.extend([(filename, heading, date, 'row_machine', line.replace("+rowing machine ", "").strip())])
        elif line.startswith("+incline dumbbells press "):
            reshaped_rows.extend([(filename, heading, date, 'inc_bells_press', line.replace("+incline dumbbells press ", "").strip())])
        elif line.startswith("+lat raises "):
            reshaped_rows.extend([(filename, heading, date, 'lat_rises', line.replace("+lat raises ", "").strip())])
        elif line.startswith("+dumbbell row "):
            reshaped_rows.extend([(filename, heading, date, 'dumbbell_row', line.replace("+dumbbell row ", "").strip())])
        elif line.startswith("+plank "):
            reshaped_rows.extend([(filename, heading, date, 'plank', line.replace("+plank ", "").strip())])
        elif line.startswith("+press and curl "):
            reshaped_rows.extend([(filename, heading, date, 'press_curl', line.replace("+press and curl ", "").strip())])
        elif line.startswith("мельдоний"):
            reshaped_rows.extend([(filename, heading, date, 'meldoniy', line.replace("мельдоний: ", "").strip())])
        elif line.startswith("feeling:"):
            reshaped_rows.extend([(filename, heading, date, 'feeling', line.replace("feeling: ", "").strip())])

    cursor.executemany('INSERT INTO reshaped_data (filename, heading, date, exercise, value) VALUES (?, ?, ?, ?, ?)', reshaped_rows)
    return len(reshaped_rows)

# Process all files in the current directory
current_directory = os.path.join(os.getcwd(), "habittracker2025-08-08")
for filename in sorted(os.listdir(current_directory)):
    if filename.endswith(".md"):  # Process only Markdown files
        logging.info(f"Processing file: {filename}")
        filepath = os.path.join(current_directory, filename)
        rows = extract_data_from_file(filepath, cursor)
        logging.info(f"{rows} has been inserted into the database.")


# Commit changes and close the database connection
conn.commit()
conn.close()

logging.info(f"Data has been successfully stored in {db_name}.")