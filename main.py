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
JSON_EXTENTION = ".json"
NO_ARTIST_MESSAGE = "No artists found in the database."
INPUT_ARTIST_NAME_MESSAGE = "Please input the name of one of the following artists: "
INVALID_CHOICE_MESSAGE = "Invalid choice."

def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file - {file_path}")
        return None

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

    print("Welcome to Mooziq!")
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
    try:
        files = os.listdir(ARTISTS_DIR)
    except FileNotFoundError:
        print(f"Error: Artists directory not found - {ARTISTS_DIR}")
        return []
    
    files.sort()
    artists = []
    for file in files:
        if file.endswith(JSON_EXTENTION):
            artists_data = load_json(os.path.join(ARTISTS_DIR, file))
            if artists_data:
                artists.append(artists_data.get("name", ""))
    return artists

def print_artists(artists):
    if artists:
        for name in artists:
            print(f"- {name}")
    else:
        print(NO_ARTIST_MESSAGE)

def get_all_artists():
    artists = read_all_artists()
    if artists:
        print("\nArtists found in the database:")
        print_artists(artists)

# !------- Task 2: Get All Albums By An Artist by Ifty -------!
def find_artist_by_name(name):
    try:
        files = sorted(os.listdir(ARTISTS_DIR))
    except FileNotFoundError:
        print(f"Error: Artists directory not found - {ARTISTS_DIR}")
        return (None, None)
    
    result = (None, None)

    for file in files:
        if file.endswith(JSON_EXTENTION):
            artist_data = load_json(os.path.join(ARTISTS_DIR, file))
            if artist_data and artist_data.get("name", "").lower() == name.lower():
                result = (file, artist_data)
    
    return result

def ordinal(num):
    num = int(num)

    if 10 <= (num % 100) <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(num % 10, "th")

    return f"{num}{suffix}"

def format_date(date_str, precision):
    parts = date_str.split("-")
    year = parts[0]

    if precision == "year":
        return f"{year}"
    
    if len(parts) > 1:
        month = int(parts[1])
    else:
        month = 1
    
    month_name = datetime(1900, month, 1).strftime("%B")

    if precision == "month":
        return f"{month_name} {year}"
    
    if len(parts) > 2:
        day = int(parts[2])
    else:
        day = 1
    
    return f"{month_name} {ordinal(day)} {year}"

def get_albums_by_artist():
    artists = read_all_artists()
    
    print_artists(artists)
    artist_name = input(INPUT_ARTIST_NAME_MESSAGE).strip()
    artist_file, artist_data = find_artist_by_name(artist_name)
    
    if artist_file:
        artist_id = artist_data.get("id")
        proper_artist_name = artist_data.get("name", artist_name)
        album_file_path = os.path.join(ALBUMS_DIR, f"{artist_id}.json")
        
        if os.path.exists(album_file_path):
            albums_data = load_json(album_file_path)
            if albums_data:
                items = albums_data.get("items", [])
                print(f"Listing all available albums from {proper_artist_name}...")

                for album in items:
                    name = album.get("name", "")
                    release_date = album.get("release_date", "")
                    release_date_precision = album.get("release_date_precision", 'day')
                    readable_date = format_date(release_date, release_date_precision)

                    print(f"- \"{name}\" was released in {readable_date}.")
        else:
            print(f"No albums found for artist '{proper_artist_name}'.")
    else:
        print(f"Artist '{artist_name}' not found.")

# !------- Task 3: Get Top Tracks By An Artist by Ifty -------!
def print_tracks(tracks, artist_name):
    print(f"Listing top tracks for {artist_name.title()}...")

    for track in tracks:
        name = track.get("name", "")
        popularity = track.get("popularity", 0)

        if popularity <= 30:
            message = "No one knows this song."
        elif popularity <= 50:
            message = "Popular song."
        elif popularity <= 70:
            message = "It is quite popular now!"
        else:
            message = "It is made for the charts!"

        print(f"- \"{name}\" has a popularity score of {popularity}. {message}")

def get_top_tracks_by_artist():
    artists = read_all_artists()

    print_artists(artists)

    artist_name = input(INPUT_ARTIST_NAME_MESSAGE).strip()
    artist_file, artist_data = find_artist_by_name(artist_name)
    
    if artist_file:
        artist_id = artist_data.get("id")
        top_file = os.path.join(TOP_TRACKS_DIR, f"{artist_id}.json")
        
        if os.path.exists(top_file):
            top_data = load_json(top_file)
            if top_data:
                tracks = top_data.get("tracks", [])
                print_tracks(tracks, artist_name)
            else:
                print(f"No top tracks found for artist '{artist_name}'.")
        else:
            print(f"No top tracks found for artist '{artist_name}'.")
    else:
        print(f"Artist '{artist_name}' not found.")

# !------- Task 4: Export Artist Data by Ifty -------!
def read_artists_data_csv():
    rows = []
    if os.path.exists(ARTISTS_DATA_CSV):
        try:
            with open(ARTISTS_DATA_CSV, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    rows.append(row)
        except (IOError, csv.Error) as error:
            print(f"Error reading CSV file: {error}")
    return rows

def write_artists_data_csv(rows):
    try:
        os.makedirs(os.path.dirname(ARTISTS_DATA_CSV), exist_ok=True)
        with open(ARTISTS_DATA_CSV, "w", encoding="utf-8", newline="") as file:
            field_names = ["artist_id", "artist_name", "number_of_albums", "top_track_1", "top_track_2", "genres"]
            writer = csv.DictWriter(file, fieldnames = field_names)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
    except IOError as error:
        print(f"Error writing to CSV file: {error}")

def get_album_count(artist_id):
    album_file = os.path.join(ALBUMS_DIR, f"{artist_id}.json")
    if os.path.exists(album_file):
        album_data = load_json(album_file)
        return len(album_data.get("items", [])) if album_data else 0

def get_top_tracks(artist_id):
    top_file = os.path.join(TOP_TRACKS_DIR, f"{artist_id}.json")
    if not os.path.exists(top_file):
        return "", ""
    
    top_data = load_json(top_file)
    if not top_data:
        return "", ""
    
    tracks = top_data.get("tracks", [])
    top1 = tracks[0].get("name", "") if len(tracks) > 0 else ""
    top2 = tracks[1].get("name", "") if len(tracks) > 1 else ""
    return top1, top2

def create_artist_row(artist_data, artist_id):
    artist_name = artist_data.get("name", "")
    num_albums = get_album_count(artist_id)
    top1, top2 = get_top_tracks(artist_id)
    genres = artist_data.get("genres", [])
    genres_str = ", ".join(genres) if genres else ""
    
    return {
        "artist_id": artist_id,
        "artist_name": artist_name,
        "number_of_albums": str(num_albums),
        "top_track_1": top1,
        "top_track_2": top2,
        "genres": genres_str
    }

def update_or_append_row(rows, artist_id, new_row):
    for row in rows:
        if row.get("artist_id", "").strip() == artist_id.strip():
            row.update(new_row)
            return True
    
    rows.append(new_row)
    return False

def export_artist_data():   
    artists = read_all_artists()
    print_artists(artists)
    artist_name_input = input(INPUT_ARTIST_NAME_MESSAGE).strip()
    
    artist_file, artist_data = find_artist_by_name(artist_name_input)
    if artist_file:
        artist_name = artist_data.get("name", artist_name_input)
        artist_id = artist_data.get("id")
        
        new_row = create_artist_row(artist_data, artist_id)
        rows = read_artists_data_csv()
        was_updated = update_or_append_row(rows, artist_id, new_row)
        
        write_artists_data_csv(rows)
        
        print(f"Exporting \"{artist_name}\" data to CSV file...")
        if was_updated:
            print("Data successfully updated.")
        else:
            print("Data successfully appended.")
    else:
        print(f"Artist '{artist_name_input}' not found.")

# !------- Task 5: Get Released Albums By Year by Salah -------!
def read_all_artists():
    files = os.listdir(ARTISTS_DIR)
    files.sort()
    artists = []
    for file in files:
        if file.endswith(JSON_EXTENTION):
            artist_data = load_json(os.path.join(ARTISTS_DIR, file))
            artist_name = artist_data.get("name", "")
            artists.append(artist_name)
    return artists

def get_main_artist(artists, main_artists):
    for artist in artists:
        name = artist.get("name", "")
        if name in main_artists:
            return name
    return ""

def collect_albums_for_years(year_input, main_artists):
    matching_albums = []
    
    for file in os.listdir(ALBUMS_DIR):
        if file.endswith(JSON_EXTENTION):
            album_path = os.path.join(ALBUMS_DIR, file)
            album_data = load_json(album_path)
            items = album_data.get("items", [])

            for album in items:
                release_date = album.get("release_date", "")
                if release_date and release_date.startswith(year_input):
                    album_name = album.get("name", "").strip()
                    artist = get_main_artist(album.get("artists", []), main_artists)
                    matching_albums.append((album_name, artist))

    return matching_albums

def sort_albums_by_name(matching_albums):
    nums = len(matching_albums)
    for index in range(nums):
        min_index = index
        for count in range(index + 1, nums):
            if matching_albums[count][0] < matching_albums[min_index][0]:
                min_index = count
        if min_index != index:
            matching_albums[index], matching_albums[min_index] = matching_albums[min_index], matching_albums[index]

def get_released_albums_by_year():
    year_input = input("Please enter a year: ").strip()

    if year_input.isdigit():
        main_artists = read_all_artists()
        matching_albums = collect_albums_for_years(year_input, main_artists)

        if matching_albums:
            sort_albums_by_name(matching_albums)

            print(f"Albums released in the year {year_input}:")
            for name, artist in matching_albums:
                print(f"- \"{name}\" by {artist}.")
        else:
            print(f"No albums were released in the year {year_input}.")
    else:
        print("Invalid year. Please enter a numeric value.")

# !------- Task 6: Analyze Song Lyrics by Ifty -------!
def get_available_songs():
    songs = []

    try:
        files = sorted(os.listdir(SONGS_DIR))
    except FileNotFoundError:
        print(f"Error: Songs directory not found - {SONGS_DIR}")
        return songs

    for file in files:
        path = os.path.join(SONGS_DIR, file)
        title = None
        artist = None
        song_data = load_json(path)
        if song_data:
            title = song_data.get("title", "")
            artist = song_data.get("artist")
            songs.append({
                "title": title,
                "artist": artist,
                "path": path,
                "type": "json"
            })
    
    seen_titles = set()
    unique_songs = []

    for song in songs:
        title = song.get("title", "Unknown")

        if title not in seen_titles:
            seen_titles.add(title)
            unique_songs.append(song)
    
    return unique_songs

def search_songs_by_keyword(entry):
    category = entry.get("type")
    path = entry.get("path")

    if category == "json":
        song_data = load_json(path)
        return song_data.get("lyrics", "") if song_data else ""
    else:
        return ""

def moosify_text(lyrics):
    moosified = lyrics
    moosified = moosified.replace("mo", "moo")
    moosified = re.sub(r"\b\w+[?!]", "moo!", moosified)
    
    return moosified

def can_be_moosified(lyrics):
    lyrics_lower = lyrics.lower()
    has_mo = "mo" in lyrics_lower
    has_punctuation = "?" in lyrics or "!" in lyrics
    
    return has_mo or has_punctuation

def print_moose():
    moose = (r""" ___            ___
/   \          /   \
\_   \        /  __/
 _\   \      /  /__
 \___  \____/   __/
     \_       _/
       | @ @  \__
       |
     _/     /\
    /o)  (o/\ \__
    \_____/ /
      \____/
""")
    print(moose)

def print_song_list(songs):
    print("Available songs:")
    for index, song in enumerate(songs, 1):
        artist = song.get("artist", "Unknown")
        title = song.get("title")
        print(f"{index}. {title} by {artist}")

def get_valid_song_choice(songs):
    choice = input("Please select one of the following songs (number): ").strip()
    
    if choice.isdigit():
        choice = int(choice) - 1
        if choice >= 0 and choice < len(songs):
            return songs[choice]
        else:
            print(INVALID_CHOICE_MESSAGE)
            return None
    else:
        print(INVALID_CHOICE_MESSAGE)
        return None

def save_moosified_lyrics(title, moosified_lyrics):
    if not os.path.exists(MOOSIFIED_DIR):
        os.makedirs(MOOSIFIED_DIR)
    
    filename = f"{title} Moosified.txt"
    file_path = os.path.join(MOOSIFIED_DIR, filename)
    
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(moosified_lyrics)
    
    return filename

def process_moosification(entry):
    title = entry.get("title")
    artist = entry.get("artist", "Unknown")
    lyrics = search_songs_by_keyword(entry)
    
    if lyrics:
        if can_be_moosified(lyrics):
            moosified_lyrics = moosify_text(lyrics)
            filename = save_moosified_lyrics(title, moosified_lyrics)
            
            print(f"{title} by {artist} has been moos-ified!")
            print(f"File saved at ./moosified/{filename}")
            print_moose()
        else:
            print(f"{title} by {artist} is not moose-compatible!")
    else:
        print(f"{title} has no lyrics available.")

def moosify_lyrics():
    songs = get_available_songs()
    
    if songs:
        print_song_list(songs)
        entry = get_valid_song_choice(songs)
        
        if entry:
            process_moosification(entry)
    else:
        print("No songs available.")

# !------- Task 7: Calculate Longest Unique Word Sequence In A Song by Ifty -------!
def process_text_for_analysis(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    words = text.split()
    return words

def print_song_list(songs):
    print("Available songs:")
    for index, song in enumerate(songs, 1):
        artist = song.get("artist", "Unknown")
        title = song.get("title")
        print(f"{index}. {title} by {artist}")

def find_longest_unique_sequence(words):
    seen = {}
    start = 0
    max_length = 0
    
    for position, word in enumerate(words):
        if word in seen and seen[word] >= start:
            start = seen[word] + 1
        
        seen[word] = position
        current_length = position - start + 1
        max_length = max(max_length, current_length)
    
    return max_length

def process_song_analysis(entry):
    title = entry.get("title")
    lyrics = search_songs_by_keyword(entry)
    
    if lyrics:
        words = process_text_for_analysis(lyrics)
        
        if words:
            max_length = find_longest_unique_sequence(words)
            print(f"The length of the longest unique sequence in {title} is {max_length}")
        else:
            print("No valid words found in the lyrics.")
    else:
        print("No lyrics found for this song.")

def calculate_longest_unique_sequence():  
    songs = get_available_songs()
    
    if songs:
        print_song_list(songs)
        entry = get_valid_song_choice(songs)
        
        if entry:
            process_song_analysis(entry)
    else:
        print("No songs available.")

# !------- Task 8: Weather Forecast For Upcoming Concerts by Salah -------!
def read_concert_data():
    concerts = []
    artists = set()

    if os.path.isfile(CONCERTS_CSV):
        try:
            with open(CONCERTS_CSV, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    artist = (row.get("artist", "")).strip()
                    city_code = (row.get("city_code", "")).strip()
                    month = row.get("month", "").strip()
                    day = row.get("day", "").strip()
                    year = row.get("year", "").strip()

                    if all([artist, city_code, month, day, year]):
                        if (month.isdigit() and day.isdigit() and year.isdigit()):
                            date = f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
                            concerts.append({"artist": artist, "city_code": city_code, "date": date})
                            artists.add(artist)
        except (IOError, csv.Error) as error:
            print(f"Error reading concerts CSV: {error}")
    else:
        print("Error: 'concerts.csv' file is missing.")

    return concerts, sorted(artists)

def read_weather_data():
    weather_fields = [
    "precipitation", "date", "city", "city_code",
    "temperature_avg", "temperature_max", "temperature_min",
    "wind_direction", "wind_speed"]
    weather_lookup = {}

    if os.path.isfile(WEATHER_CSV):
        try:
            with open(WEATHER_CSV, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    city_code = (row.get("city_code", "")).strip()
                    date = (row.get("date", "")).strip()

                    if city_code and date:
                        key = (city_code, date)
                        weather_lookup[key] = {
                            field: (row.get(field, "")).strip()
                            for field in weather_fields
                        }
        except (IOError, csv.Error) as error:
            print(f"Error reading weather CSV: {error}")
    else:
        print("Error: 'weather.csv' file is missing.")

    return weather_lookup

def forecast_message(weather):
    messages = []

    try:
        precipitation = float(weather.get("precipitation", "0"))
        temp_min = float(weather.get("temperature_min", "0"))
        wind_speed = float(weather.get("wind_speed", "0"))
    except ValueError:
        return "No data."

    if temp_min <= 10:
        messages.append("Wear warm clothes.")

    if precipitation >= 2.3:
        if wind_speed < 15:
            messages.append("Bring an umbrella.")
        else:
            messages.append("Bring a raincoat.")

    if temp_min > 10 and precipitation < 2.3:
        messages.append("Perfect weather!")

    return " ".join(messages)

def print_concert_weather(concert, weather_data):
    key = (concert["city_code"], concert["date"])
    weather = weather_data.get(key)
    
    if weather:
        city = weather.get("city", "Unknown City")
        formatted_date = format_date(concert["date"], "day")
        message = forecast_message(weather)
        print(f"- {city}, {formatted_date}. {message}")
    else:
        print(f"- {concert['city_code']}, {concert['date']}. Weather data not available.")

def predict_weather_for_concerts():
    concerts, artist_list = read_concert_data()
    weather_data = read_weather_data()
    
    if concerts:
        print("Upcoming artists:")
        print_artists(artist_list)
        
        artist_input = input(INPUT_ARTIST_NAME_MESSAGE).strip()
        matching_concerts = [c for c in concerts if c["artist"].lower() == artist_input.lower()]
        
        if matching_concerts:
            formatted_artist = next((a for a in artist_list if a.lower() == artist_input.lower()), artist_input)
            concert_word = "concert" if len(matching_concerts) == 1 else "concerts"
            
            print(f"Fetching weather forecast for \"{formatted_artist}\" concerts...")
            print(f"{formatted_artist} has {len(matching_concerts)} upcoming {concert_word}:")
            
            for concert in matching_concerts:
                print_concert_weather(concert, weather_data)
        else:
            print(f"No upcoming concerts found for '{artist_input}'.")
    else:
        print("No upcoming concerts found.")

# !------- Task 9: Search Song By Lyrics by Ifty -------!
def add_song_to_index(song_data, inverted_index):
    title = song_data.get("title", "")
    lyrics = song_data.get("lyrics", "")
    
    if lyrics and title:
        words = process_text_for_analysis(lyrics)
        
        for word in words:
            if word not in inverted_index:
                inverted_index[word] = []
            if title not in inverted_index[word]:
                inverted_index[word].append(title)

def build_inverted_index():
    inverted_index = {}
    
    try:
        files = os.listdir(SONGS_DIR)
    except FileNotFoundError:
        print(f"Error: Songs directory not found - {SONGS_DIR}")
        return inverted_index
    
    for file in files:
        if file.endswith(JSON_EXTENTION):
            song_path = os.path.join(SONGS_DIR, file)
            song_data = load_json(song_path)
            if song_data:
                add_song_to_index(song_data, inverted_index)
    
    return inverted_index

def load_or_create_inverted_index():
    if os.path.exists(INVERTED_INDEX_FILE):
        inverted_index = load_json(INVERTED_INDEX_FILE)
        if inverted_index:
            return inverted_index
    
    inverted_index = build_inverted_index()
    
    try:
        os.makedirs(os.path.dirname(INVERTED_INDEX_FILE), exist_ok=True)
        with open(INVERTED_INDEX_FILE, "w", encoding="utf-8") as file:
            json.dump(inverted_index, file, indent=2)
    except IOError as error:
        print(f"Warning: Could not save inverted index: {error}")
    
    return inverted_index

def calculate_song_scores(query_words, inverted_index):
    song_scores = {}
    
    for word in query_words:
        if word in inverted_index:
            for song in inverted_index[word]:
                song_scores[song] = song_scores.get(song, 0) + 1
    return song_scores

def search_by_lyrics():
    query = input("Please type the lyrics you'd like to search for: ").strip()
    
    if query:
        query_words = process_text_for_analysis(query)
        
        if query_words:
            inverted_index = load_or_create_inverted_index()
            song_scores = calculate_song_scores(query_words, inverted_index)
            
            if song_scores:
                sorted_songs = sorted(song_scores.items(), reverse=True)
                
                print(f"Listing matches for '{query}'...")
                for song, score in sorted_songs:
                    print(f"- {song} with a score of {score}")
            else:
                print(f"No matches found for '{query}'.")
        else:
            print("Invalid search query.")
    else:
        print("Please enter a valid search query.")

if __name__ == "__main__":
    main()