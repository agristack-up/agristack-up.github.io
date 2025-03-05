import json
import csv

# File names
json_file = "games.json"  # JSON file
csv_file = "iframe_results.csv"     # CSV file

# JSON file read karein
with open(json_file, "r", encoding="utf-8") as file:
    data = json.load(file)

# Track karein ki kaunse games ka URL update ho chuka hai
updated_games = set()

# CSV file se naye URLs read karein aur replace karein
with open(csv_file, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    for row in reader:
        if len(row) == 2:  # Ensure row has both game name and new URL
            game_name, new_url = row
            if game_name in data and game_name not in updated_games:
                data[game_name] = new_url  # JSON me URL update karein
                updated_games.add(game_name)  # Is game ko updated list me daal dein

# Updated JSON wapas likhein
with open(json_file, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)

print("URLs successfully replaced! Duplicate entries ignored.")
