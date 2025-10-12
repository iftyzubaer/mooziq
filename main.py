import os
import json
import csv
import re
from datetime import datetime

# !------- Helper utilities by Ifty Zubaer -------!
ROOT = os.path.dirname(os.path.abspath(__file__))
DATASET = os.path.join(ROOT, "dataset")
MOOSIFIED_DIR = os.path.join(ROOT, "moosified")
ARTISTS_DATA_CSV = os.path.join(DATASET, "artist-data.csv")
INVERTED_INDEX_FILE = os.path.join(DATASET, "inverted_index.json")
CONCERTS_CSV = os.path.join(DATASET, "concerts", "concerts.csv")
WEATHER_CSV = os.path.join(DATASET, "weather", "weather.csv")
ARTISTS_DIR = os.path.join(DATASET, "artists")
ALBUMS_DIR = os.path.join(DATASET, "albums")
TOP_TRACKS_DIR = os.path.join(DATASET, "top_tracks")
LYRICS_DIR = os.path.join(DATASET, "lyrics")
SONGS_DIR = os.path.join(DATASET, "songs")

def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# For task 6 and 7
def get_available_songs():
    songs = []

    for file in sorted(os.listdir(SONGS_DIR)):
        path = os.path.join(SONGS_DIR, file)
        title = None
        artist = None

        if file.endswith(".txt"):
            name = os.path.splitext(file)[0]
            title = name
            songs.append({
                "title": title,
                "artist": artist,
                "path": path,
                "type": "txt"
            })
        elif file.endswith(".json"):
            song_data = load_json(path)
            title = song_data.get("name", "") or song_data.get("title", "") or os.path.splitext(file)[0]
            artist = song_data.get("artist")
            songs.append({
                "title": title,
                "artist": artist,
                "path": path,
                "type": "json"
            })
    
    if not songs:
        for file in sorted(os.listdir(SONGS_DIR)):
            if file.endswith(".json"):
                song_data = load_json(os.path.join(SONGS_DIR, file))
                title = song_data.get("name", "")
                artist = song_data.get("artist")
                lyrics = song_data.get("lyrics", "")
                songs.append({
                    "title": title,
                    "artist": artist,
                    "path": os.path.join(SONGS_DIR, file),
                    "type": "songjson",
                    "lyrics": lyrics
                })
    
    seen_titles = set()
    unique_songs = []

    for song in songs:
        title = song.get("title") or "Unknown"

        if title not in seen_titles:
            seen_titles.add(title)
            unique_songs.append(song)
    
    return unique_songs

# For task 6 and 7
def search_songs_by_keyword(entry):
    category = entry.get("type")
    path = entry.get("path")

    if category == "txt":
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    elif category == "json":
        song_data = load_json(path)
        return song_data.get("lyrics", "")
    elif category == "songjson":
        if entry.get("lyrics"):
            return entry.get("lyrics")
        song_data = load_json(path)
        return song_data.get("lyrics", "")
    else:
        return ""

# !------- Task 0.1: Main Menu by Ifty Zubaer -------!
def print_menu():
    
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

    print("\nWelcome to Mooziq!")
    print("Choose one of the options bellow:\n")

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
                    calculate_longest_unique_sequence()
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
    files.sort()
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

# !------- Task 2: Get All Albums By An Artist by Ifty -------!
def find_artist_by_name(name):
    files = sorted(os.listdir(ARTISTS_DIR))
    result = (None, None)

    for file in files:
        if file.endswith(".json"):
            artist_data = load_json(os.path.join(ARTISTS_DIR, file))
            if artist_data.get("name", "").lower() == name.lower():
                result = (file, artist_data)
    
    return result

def ordinal(num):
    num = int(num)

    if 10 <= (num % 100) <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(num % 10, 'th')

    return f"{num}{suffix}"

def formated_date(date_str, precision):
    parts = date_str.split('-')
    year = parts[0]

    if precision == 'year':
        return f"{year}"
    
    if len(parts) > 1:
        month = int(parts[1])
    else:
        month = 1
    
    month_name = datetime(1900, month, 1).strftime('%B')

    if precision == 'month':
        return f"{month_name} {year}"
    
    if len(parts) > 2:
        day = int(parts[2])
    else:
        day = 1
    
    return f"{month_name} {ordinal(day)} {year}"

def get_albums_by_artist():
    artist_name = input("Please input the name of an artist: ").strip()
    artist_file, artist_data = find_artist_by_name(artist_name)
    
    if artist_file:
        artist_id = artist_data.get("id")
        proper_artist_name = artist_data.get("name", artist_name)
        album_file_path = os.path.join(ALBUMS_DIR, f"{artist_id}.json")
        
        if os.path.exists(album_file_path):
            albums_data = load_json(album_file_path)
            items = albums_data.get("items", [])
            print(f"Listing all available albums from {proper_artist_name}...")

            for album in items:
                name = album.get("name", "")
                release_date = album.get("release_date", "")
                release_date_precision = album.get("release_date_precision", 'day')
                readable_date = formated_date(release_date, release_date_precision)

                print(f"- \"{name}\" was released in {readable_date}.")

# !------- Task 3: Get Top Tracks By An Artist by Ifty -------!
def get_top_tracks_by_artist():
    artist_name = input("Please input the name of an artist: ").strip()
    artist_file, artist_data = find_artist_by_name(artist_name)
    
    if not artist_file:
        print(f"Artist '{artist_name}' not found.")
        return
    
    artist_id = artist_data.get('id')
    top_file = os.path.join(TOP_TRACKS_DIR, f"{artist_id}.json")
    
    if not os.path.exists(top_file):
        print(f"No top tracks found for artist '{artist_name}'.")
        return
    
    top_data = load_json(top_file)
    tracks = top_data.get('tracks', [])
    print(f"Listing top tracks for {artist_name}...")

    for track in tracks:
        name = track.get('name', '')
        popularity = track.get('popularity', 0)

        if popularity <= 30:
            message = "No one knows this song."
        elif popularity <= 50:
            message = "Popular song."
        elif popularity <= 70:
            message = "It is quite popular now!"
        else:
            message = "It is made for the charts!"

        print(f"- \"{name}\" has a popularity score of {popularity}. {message}")

# !------- Task 4: Export Artist Data by Ifty -------!
def read_artists_data_csv():
    rows = []
    if os.path.exists(ARTISTS_DATA_CSV):
        with open(ARTISTS_DATA_CSV, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                rows.append(row)
    return rows

def write_artists_data_csv(rows):
    with open(ARTISTS_DATA_CSV, "w", encoding="utf-8", newline="") as file:
        field_names = ["artist_id", "artist_name", "number_of_albums", "top_track_1", "top_track_2", "genres"]
        writer = csv.DictWriter(file, fieldnames = field_names)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

def export_artist_data():
    artists = read_all_artists()
    for name in artists:
        print(f"- {name}")
    artist_name_input = input("Please input the name of one of the following artists: ").strip()

    artist_file, artist_data = find_artist_by_name(artist_name_input)
    if artist_file:
        artist_name = artist_data.get("name", artist_name_input)
        artist_id = artist_data.get("id")

        album_file = os.path.join(ALBUMS_DIR, f"{artist_id}.json")
        num_albums = 0
        if os.path.exists(album_file):
            album_data = load_json(album_file)
            num_albums = len(album_data.get("items", []))

        top_file = os.path.join(TOP_TRACKS_DIR, f"{artist_id}.json")
        top1 = top2 = ""
        if os.path.exists(top_file):
            top_data = load_json(top_file)
            tracks = top_data.get("tracks", [])
            if len(tracks) > 0:
                top1 = tracks[0].get("name", "")
            if len(tracks) > 1:
                top2 = tracks[1].get("name", "")

        genres = artist_data.get("genres", [])
        genres_str = ", ".join(genres) if genres else ""

        rows = read_artists_data_csv()
        found = False
        for row in rows:
            if row.get("artist_id", "").strip() == artist_id.strip():
                row["artist_name"] = artist_name
                row["number_of_albums"] = str(num_albums)
                row["top_track_1"] = top1
                row["top_track_2"] = top2
                row["genres"] = genres_str
                found = True

        if not found:
            rows.append({
                "artist_id": artist_id,
                "artist_name": artist_name,
                "number_of_albums": str(num_albums),
                "top_track_1": top1,
                "top_track_2": top2,
                "genres": genres_str
            })

        write_artists_data_csv(rows)

        print(f"Exporting \"{artist_name}\" data to CSV file...")
        if found:
            print("Data successfully updated.")
        else:
            print("Data successfully appended.")

# !------- Task 5: Get Released Albums By Year by Salah -------!
def get_released_albums_by_year():
    pass

# !------- Task 6: Analyze Song Lyrics by Ali -------!
def moosify_lyrics():
    pass

# !------- Task 7: Calculate Longest Unique Word Sequence In A Song by Ifty -------!
def propocess_text_for_analysis(text):
    text = text.lower()
    text = re.sub(r"[^\w\s']", " ", text)
    text = re.sub(r"\s+", " ", text)
    words = text.strip().split()

    return words

def calculate_longest_unique_sequence():
    songs = get_available_songs()

    if songs:
        print("Available songs:")

        for index, song in enumerate(songs):
            artist = song.get("artist") or "Unknown"
            print(f"{index + 1}. {song.get('title')} by {artist}")
        
        choice = input("Please select one of the following songs (number): ").strip()
        
        if choice.isdigit():
            choice = int(choice)

            if choice < 1 or choice > len(songs):
                print("Invalid choice.")
                return
            
            entry = songs[choice - 1]
            lyrics = search_songs_by_keyword(entry)

            if lyrics:
                words = propocess_text_for_analysis(lyrics)
                seen = {}
                start = 0
                max_len = 0

                for end in range(len(words)):
                    word = words[end]
                    if word in seen:
                        start = max(start, seen[word] + 1)
                    
                    seen[word] = end
                    max_len = max(max_len, end - start + 1)
                
                print(f"The length of the longest unique sequence in {entry.get('title')} is {max_len}")
        else:
            print("Invalid input.")

# !------- Task 8: Weather Forecast For Upcoming Concerts by Salah -------!
def predict_weather_for_concerts():
    pass

# !------- Task 9: Search Song By Lyrics by Ali -------!
def search_by_lyrics():
    pass

if __name__ == "__main__":
    main()