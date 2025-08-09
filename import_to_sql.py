import os
import sqlite3
from datetime import datetime

# Create SQLite database and table
db_name = "habit_tracker.db"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()
NOISE = ["> something to do:",
        "someone to love:",
        "something to hope for:",
        ">",
        "Вопросы для саморефлексии:",
        "1. провалиться или не попробовать?",
        "2. что я принимаю как должное?",
        "3. держусь ли я за то, что нужно отпустить ?",
        "4. Держу ли я фокус на том, что действительно важно?",
        "5. Если не сейчас то когда ?"]

# cursor.execute('''
# CREATE TABLE IF NOT EXISTS habit_data (
#     filename TEXT PRIMARY KEY,
#     heading TEXT,
#     date TEXT,
#     bench_press TEXT,
#     bench_press_2 TEXT,
#     bench_press_3 TEXT,
#     pull_down TEXT,
#     seated_row TEXT,
#     triceps TEXT,
#     Bulgarian_Squat TEXT,
#     Leg_extension TEXT,
#     Leg_curl TEXT,
#     Leg_press TEXT,
#     Calf_extension TEXT,
#     fitband_duration TEXT,
#     fitband_kcal TEXT,
#     fitband_heartrate TEXT,
#     full_text TEXT,
#     row_machine TEXT,
#     inc_bells_press TEXT,
#     lat_rises TEXT
# )
# ''')
# conn.commit()

# Function to extract required data from a file
def extract_data_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        filename = os.path.basename(filepath)
        heading = lines[0].strip("# ").strip() if lines else None
        date = None
        row_machine = None
        bench_press = None
        bench_press_2 = None
        bench_press_3 = None
        pull_down = None
        seated_row = None
        triceps = None
        Bulgarian_Squat = None
        Leg_extension = None
        Leg_curl = None
        Leg_press = None
        Calf_extension = None
        fitband_duration = None
        fitband_kcal = None
        fitband_heartrate = None
        inc_bells_press = None
        lat_rises = None
        dumbbell_row = None
        plank = None
        press_curl = None
        full_text = "".join([line for line in lines if line.strip() and line.strip() not in NOISE])
        
        for line in lines:
            line = line.lower()
            if line.startswith("date:"):
                # Extract and convert date to ISO 8601 format
                raw_date = line.split(":", 1)[1].strip()
                try:
                    date = datetime.strptime(raw_date, "%m/%d/%Y").strftime("%Y-%m-%d")
                except ValueError:
                    date = None  # Handle invalid date format
            elif line.lstrip("+").startswith("жим от груди") and \
                    not line.lstrip("+").startswith("жим от груди 2") and \
                    not line.lstrip("+").startswith("жим от груди 3"):
                bench_press = line.replace("жим от груди ", "").strip()
            elif line.lstrip("+").startswith("жим от груди 2"):
                bench_press_2 = line.replace("жим от груди ", "").strip()
            elif line.lstrip("+").startswith("жим от груди 3"):
                bench_press_3 = line.replace("жим от груди 3поз стула", "").strip()
            elif line.lstrip("+").startswith("pull down"):
                pull_down = line.replace("pull down ", "").strip()
            elif line.lstrip("+").startswith("seated row"):
                seated_row = line.replace("seated row ", "").strip()
            elif line.lstrip("+").startswith("трицепс "):
                triceps = line.replace("трицепс ", "").strip()
            elif line.lstrip("**").lstrip("+").startswith("bulgarian split squat**"):
                Bulgarian_Squat = line.replace("**", "").replace("bulgarian split squat", "").strip()
            elif line.lstrip("+").startswith("leg extension") and not line == "leg extension - показалось что болгарские более общие чем это.\n":
                Leg_extension = line.replace("leg extension", "").strip()
            elif line.lstrip("+").startswith("leg curl"):
                Leg_curl = line.replace("leg curl", "").strip()
            elif line.lstrip("+").startswith("leg press"):
                Leg_press = line.replace("leg press", "").strip()
            elif line.lstrip("+").startswith("calf extension"):
                Calf_extension = line.replace("calf extension", "").strip()
            elif line.startswith("duration") and not line.startswith("duration 0:00:00"):
                fitband_duration = line.split(" ", 1)[1].strip()
            elif " kcal" in line and not line == "00 kcal\n":
                fitband_kcal = line.split(" ", 1)[0].strip()
            elif line.startswith("heart rate") and not line == "heart rate 0 avg, 0 max (aerobic 0min)\n":
                fitband_heartrate = line.replace("heart rate", "").strip()
            elif line.lstrip("+").startswith("rowing machine "):
                row_machine = line.lstrip("+").replace("rowing machine ", "").strip()
            elif line.lstrip("+").startswith("incline dumbbells press "):
                inc_bells_press = line.lstrip("+").replace("incline dumbbells press ", "").strip()
            elif line.lstrip("+").startswith("lat raises "):
                lat_rises = line.lstrip("+").replace("lat raises ", "").strip()
            elif line.lstrip("+").startswith("dumbbell row "):
                dumbbell_row = line.lstrip("+").replace("dumbbell row ", "").strip()
            elif line.lstrip("+").startswith("plank "):
                plank = line.lstrip("+").replace("plank ", "").strip()
            elif line.lstrip("+").startswith("press and curl "):
                press_curl = line.lstrip("+").replace("press and curl ", "").strip()

        return filename, heading, date, bench_press, bench_press_2, bench_press_3, pull_down, seated_row, \
            triceps, Bulgarian_Squat, Leg_extension, Leg_curl, Leg_press, Calf_extension, fitband_duration, \
            fitband_kcal, fitband_heartrate, full_text, row_machine, inc_bells_press, lat_rises, \
            dumbbell_row, plank, press_curl

# Process all files in the current directory
current_directory = os.path.join(os.getcwd(), "habittracker2025-08-08")
for filename in os.listdir(current_directory):
    if filename.endswith(".md"):  # Process only Markdown files
        filepath = os.path.join(current_directory, filename)
        data = extract_data_from_file(filepath)
        cursor.execute('''
        INSERT OR IGNORE INTO habit_data (filename, heading, date,
        bench_press, bench_press_2, bench_press_3, pull_down, seated_row, triceps,
        Bulgarian_Squat, Leg_extension, Leg_curl, Leg_press, Calf_extension,
        fitband_duration, fitband_kcal, fitband_heartrate, full_text, row_machine,
        inc_bells_press, lat_rises)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)


# Commit changes and close the database connection
conn.commit()
conn.close()

print(f"Data has been successfully stored in {db_name}.")