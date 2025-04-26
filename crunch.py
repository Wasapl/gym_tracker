import sqlite3
import re


# Connect to the SQLite database
db_name = "habit_tracker.db"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Step 1: Add new columns to the table if they don't already exist
columns_to_add = [
  # bench_press
  ("bp_avg", "REAL"),
  ("bp_max", "REAL"),
  # bench_press_2
  ("bp_2_avg", "REAL"),
  ("bp_2_max", "REAL"),
  # bench_press_3
  ("bp_3_avg", "REAL"),
  ("bp_3_max", "REAL"),
  # pull_down
  ("pd_avg", "REAL"),
  ("pd_max", "REAL"),
  # seated_row
  ("sr_avg", "REAL"),
  ("sr_max", "REAL"),
  # triceps
  ("triceps_avg", "REAL"),
  ("triceps_max", "REAL"),
  # Bulgarian_Squat
  ("Bulgarian_Squat_avg", "REAL"),
  ("Bulgarian_Squat_max", "REAL"),
  # Leg_extension
  ("Leg_extension_avg", "REAL"),
  ("Leg_extension_max", "REAL"),
  # Leg_curl
  ("Leg_curl_avg", "REAL"),
  ("Leg_curl_max", "REAL"),
  # Leg_press
  ("Leg_press_avg", "REAL"),
  ("Leg_press_max", "REAL"),
  # Calf_extension
  ("Calf_extension_avg", "REAL"),
  ("Calf_extension_max", "REAL"),
  # Heart_rate
  ("heart_rate_avg", "REAL"),
  ("heart_rate_max", "REAL"),
  # aerobic
  ("aerobic_minutes", "REAL"),

]

for column_name, column_type in columns_to_add:
  try:
    cursor.execute(f"ALTER TABLE habit_data ADD COLUMN {column_name} {column_type}")
  except sqlite3.OperationalError:
    pass
    # print(f"Column {column_name} already exists.")



# Query to select date and bench_press from the habit_data table
query = ("SELECT filename, date, bench_press, bench_press_2, bench_press_3, pull_down, seated_row, triceps, "
         " Bulgarian_Squat, Leg_extension, Leg_curl, Leg_press, Calf_extension, fitband_heartrate "
         " FROM habit_data order by date desc")
cursor.execute(query)
rows = cursor.fetchall()

def crunch(stat: str):
  try:
    cleared = stat.lstrip("+").replace("lbs", "").replace("лбс", "").replace("лб", "").replace("(смит) ", "").strip()
    multiplied = []
    for pair in cleared.split(","):
      pair = pair.strip()
      weight, reps = pair.split(" ")
      for r in reps.split("-"):
        if r.isdigit():
          multiplied.append(int(weight) * int(r))
    average = round(sum(multiplied) / len(multiplied), 0) if multiplied else 0
    max_weight = max(multiplied) if multiplied else 0
    return average, max_weight
  except Exception as e:
    print(f"Error processing stat: {stat}, Error: {e}")
    print(f"Cleared: {cleared}")
    print(f"pair: {pair}, weight: {weight}, reps: {reps}")
    print(f"multiplied: {multiplied}")
    print(f"rep: {r}")

def heartrate(stat: str):
  cleared = stat.lstrip("+").strip()
  match = re.match(r"(\d+)\s*avg,\s*(\d+)\s*max\s*\(aerobic\s*(\d+)min\)", cleared)
  if match:
    heart_rate_avg = int(match.group(1))
    heart_rate_max = int(match.group(2))
    aerobic_minutes = int(match.group(3))
    return heart_rate_avg, heart_rate_max, aerobic_minutes
  else:
    return None, None, None



# Print the results
for row in rows:
    row_id, date, bench_press, bench_press_2, bench_press_3, pull_down, seated_row, triceps, \
       Bulgarian_Squat, Leg_extension, Leg_curl, Leg_press, Calf_extension, fitband_heartrate = row
    if date:
      bp_avg, bp_max = crunch(bench_press) if bench_press else (None, None)
      bp_2_avg, bp_2_max = crunch(bench_press_2) if bench_press_2 else (None, None)
      bp_3_avg, bp_3_max = crunch(bench_press_3) if bench_press_3 else (None, None)
      pd_avg, pd_max = crunch(pull_down) if pull_down else (None, None)
      sr_avg, sr_max = crunch(seated_row) if seated_row else (None, None)
      triceps_avg, triceps_max = crunch(triceps) if triceps else (None, None)
      Bulgarian_Squat_avg, Bulgarian_Squat_max = crunch(Bulgarian_Squat) if Bulgarian_Squat else (None, None)
      Leg_extension_avg, Leg_extension_max = crunch(Leg_extension) if Leg_extension else (None, None)
      Leg_curl_avg, Leg_curl_max = crunch(Leg_curl) if Leg_curl else (None, None)
      Leg_press_avg, Leg_press_max = crunch(Leg_press) if Leg_press else (None, None)
      Calf_extension_avg, Calf_extension_max = crunch(Calf_extension) if Calf_extension else (None, None)
      heart_rate_avg, heart_rate_max, aerobic_minutes = heartrate(fitband_heartrate) if fitband_heartrate else (None, None, None)
      # print(f"Date: {date}, Bench Press: {bench_press}, BP_Avg: {bp_avg}, BP_Max: {bp_max}")
      cursor.execute(
          ("UPDATE habit_data SET bp_avg = ?, bp_max = ?, "
          "bp_2_avg = ?, bp_2_max = ?, bp_3_avg = ?, bp_3_max = ?, "
          "pd_avg = ?, pd_max = ?, sr_avg = ?, sr_max = ?, "
          "triceps_avg = ?, triceps_max = ?, "
          "Bulgarian_Squat_avg = ?, Bulgarian_Squat_max = ?, "
          "Leg_extension_avg = ?, Leg_extension_max = ?, "
          "Leg_curl_avg = ?, Leg_curl_max = ?, "
          "Leg_press_avg = ?, Leg_press_max = ?, "
          "Calf_extension_avg = ?, Calf_extension_max = ?, "
          "heart_rate_avg = ?, heart_rate_max = ?, "
          "aerobic_minutes = ? "
          "WHERE filename = ?"),
          (bp_avg, bp_max, bp_2_avg, bp_2_max, bp_3_avg, bp_3_max,
          pd_avg, pd_max, sr_avg, sr_max, triceps_avg, triceps_max,
          Bulgarian_Squat_avg, Bulgarian_Squat_max,
          Leg_extension_avg, Leg_extension_max,
          Leg_curl_avg, Leg_curl_max,
          Leg_press_avg, Leg_press_max,
          Calf_extension_avg, Calf_extension_max,
          heart_rate_avg, heart_rate_max, aerobic_minutes,
          row_id)
      )

# Close the database connection
conn.commit()
conn.close()

print("Table updated.")