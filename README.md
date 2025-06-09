# Habit tracker conversion
Convert from Notion page to spreadsheet.
still need to find out a better format for spreadsheet.

## Flow of data
```mermaid
flowchart LR
  Notion --import_to_sql--> sqliteDB
  F[calculated fields] --crunch.-->sqliteDB
  sqliteDB --> GS[Google spreadsheet]
```


## News
### 2025-06-09
- updated from Notion to SQLite
- fixed import of row machine line
- `all_data` google Sheet and table view
- added `Incline dumbbells press` and `Lat raises` columns to `all_data` sheet

### 2025-05-29
- updated from Notion to SQLite
- shuffled fields in `all data` google Sheet to group data together.
- new view in SQLite to reflect shuffled fields in Google sheet

### 2025-05-25
- Updated from Notion to Sqllite.
- All fields in Sqlite are amended.
- crunching all fields

### 2025-05-05
- Updated from Notion to Sqllite.
- All fields in Sqlite are amended.
TODO:
  - add more calculable fields to crunch.py and run it.
  - Duplicate sheet in spreadsheet and populate it with updated numbers. check difference between two sheets



# Bits
rename markdown files exported from Notion:
```bash
for a in *.md; do
  if [[ ! "$a" =~ ^20 ]]; then
    d=$(grep -hE "^Date: " "$a" | cut -d" " -f2 | gsed -E "s|([0-9]{2})/([0-9]{2})/([0-9]{4})|\\3-\\1-\\2|")
    echo mv "$a" "$d-$a"
    mv "$a" "$d-$a"
  fi
done
```

