import os
import json
import csv
import re
from datetime import datetime

# !------- Helper utilities by Ifty Zubaer -------!
ROOT = os.path.dirname(os.path.abspath(__file__))
DATASET = os.path.join(ROOT, "dataset")
MOOSIFIED_DIR = os.path.join(ROOT, "moosified")
ARTISTS_DATA_CSV = os.path.join(DATASET, "artists-data.csv")
INVERTED_INDEX_FILE = os.path.join(DATASET, "inverted_index.json")
CONCERTS_CSV = os.path.join(DATASET, "concerts", "concerts.csv")
WEATHER_CSV = os.path.join(DATASET, "weather", "weather.csv")
ARTISTS_DIR = os.path.join(DATASET, "artists")
ALBUMS_DIR = os.path.join(DATASET, "albums")
TOP_TRACKS_DIR = os.path.join(DATASET, "top_tracks")
LYRICS_DIR = os.path.join(DATASET, "lyrics")
SONGS_DIR = os.path.join(DATASET, "songs")

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# !------- Task 0.1: Main Menu by Ifty Zubaer -------!
def print_menu():
    print("\nWelcome to Mooziq!")
    print("Choose one of the options below:\n")
    print("1. Get All Artists")
    print("2. Get All Albums By An Artist")
    print("3. Get Top Tracks By An Artist")
    print("4. Export Artist Data")
    print("5. Get Released Albums By Year")
    print("6. Analyze Song Lyrics")
    print("7. Calculate Longest Unique Word Sequence In A Song")
    print("8. Weather Forecast For Upcoming Concerts")
    print("9. Search Song By Lyrics")
    print("10. Exit\n")

def main():
    option = 0
    while option != 10:
        print_menu()
        option_input = input("Type your option: ").strip()
        if option_input.isdigit():
            option = int(option_input)
            match option:
                case 1:
                    get_all_artists()
                case 2:
                    get_albums_by_artist()
                case 3:
                    get_top_tracks_by_artist()
                case 4:
                    export_artist_data()
                case 5:
                    get_released_albums_by_year()
                case 6:
                    moosify_lyrics()
                case 7:
                    detect_longest_unique_sequence()
                case 8:
                    predict_weather_for_concerts()
                case 9:
                    search_by_lyrics()
                case 10:
                    print("Thank you for using Mooziq! Have a nice day :)")
                case _:
                    print("Error - Invalid option. Please input a number between 1 and 10.")
        else:
            print("Error - Invalid option. Please input a number between 1 and 10.")

# !------- Task 1: Get All Artists by Ifty -------!
def read_all_artists():
    files = os.listdir(ARTISTS_DIR)
    artists = []
    for file in files:
        if file.endswith(".json"):
            artists_data = load_json(os.path.join(ARTISTS_DIR, file))
            artists.append(artists_data.get("name", "Unknown Artist"))
    
    return artists

def get_all_artists():
    artists = read_all_artists()
    print("Artists found in the database:")
    for name in artists:
        print(f"- {name}")

# !------- Task 2: Get All Albums By An Artist by Salah -------!
def get_albums_by_artist():
    pass
# !------- Task 3: Get Top Tracks By An Artist by Ali -------!
def get_top_tracks_by_artist():
    pass
# !------- Task 4: Export Artist Data by Ifty -------!
def export_artist_data():
    pass
# !------- Task 5: Get Released Albums By Year by Salah -------!
def get_released_albums_by_year():
    pass
# !------- Task 6: Analyze Song Lyrics by Ali -------!
def moosify_lyrics():
    pass
# !------- Task 7: Calculate Longest Unique Word Sequence In A Song by Ifty -------!
def detect_longest_unique_sequence():
    pass
# !------- Task 8: Weather Forecast For Upcoming Concerts by Salah -------!
def predict_weather_for_concerts():
    pass
# !------- Task 9: Search Song By Lyrics by Ali -------!
def search_by_lyrics():
    pass

if __name__ == "__main__":
    main()