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
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file - {file_path}")
        return None

# For task 6 and 7
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
            if song_data:
                title = song_data.get("name", "") or song_data.get("title", "") or os.path.splitext(file)[0]
                artist = song_data.get("artist")
                songs.append({
                    "title": title,
                    "artist": artist,
                    "path": path,
                    "type": "json"
                })
    
    if not songs:
        for file in files:
            if file.endswith(".json"):
                song_data = load_json(os.path.join(SONGS_DIR, file))
                if song_data:
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
        try:
            with open(path, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error: File not found - {path}")
            return ""
    elif category == "json":
        song_data = load_json(path)
        return song_data.get("lyrics", "") if song_data else ""
    elif category == "songjson":
        if entry.get("lyrics"):
            return entry.get("lyrics")
        song_data = load_json(path)
        return song_data.get("lyrics", "") if song_data else ""
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
        if file.endswith(".json"):
            artists_data = load_json(os.path.join(ARTISTS_DIR, file))
            if artists_data:
                artists.append(artists_data.get("name", "Unknown Artist"))
    return artists

def get_all_artists():
    artists = read_all_artists()
    if artists:
        print("\nArtists found in the database:")
        for name in artists:
            print(f"- {name}")
    else:
        print("No artists found in the database.")

# !------- Task 2: Get All Albums By An Artist by Ifty -------!
def find_artist_by_name(name):
    try:
        files = sorted(os.listdir(ARTISTS_DIR))
    except FileNotFoundError:
        print(f"Error: Artists directory not found - {ARTISTS_DIR}")
        return (None, None)
    
    result = (None, None)

    for file in files:
        if file.endswith(".json"):
            artist_data = load_json(os.path.join(ARTISTS_DIR, file))
            if artist_data and artist_data.get("name", "").lower() == name.lower():
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
    artists = read_all_artists()
    
    if artists:
        for name in artists:
            print(f"- {name}")
    else:
        print("No artists found in the database.")

    artist_name = input("Please input the name of one of the following artists: ").strip()
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
                    readable_date = formated_date(release_date, release_date_precision)

                    print(f"- \"{name}\" was released in {readable_date}.")
        else:
            print(f"No albums found for artist '{proper_artist_name}'.")
    else:
        print(f"Artist '{artist_name}' not found.")

# !------- Task 3: Get Top Tracks By An Artist by Ifty -------!
def get_top_tracks_by_artist():
    artists = read_all_artists()
    
    if artists:
        for name in artists:
            print(f"- {name}")
    else:
        print("No artists found in the database.")

    artist_name = input("Please input the name of one of the following artists: ").strip()
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
    if not top_data:
        print(f"No top tracks found for artist '{artist_name}'.")
        return
    
    tracks = top_data.get('tracks', [])
    print(f"Listing top tracks for {artist_name.title()}...")

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
        try:
            with open(ARTISTS_DATA_CSV, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    rows.append(row)
        except (IOError, csv.Error) as e:
            print(f"Error reading CSV file: {e}")
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
    except IOError as e:
        print(f"Error writing to CSV file: {e}")

def export_artist_data():
    artists = read_all_artists()
    if not artists:
        print("No artists found in the database.")
        return
    
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
            if album_data:
                num_albums = len(album_data.get("items", []))

        top_file = os.path.join(TOP_TRACKS_DIR, f"{artist_id}.json")
        top1 = top2 = ""
        if os.path.exists(top_file):
            top_data = load_json(top_file)
            if top_data:
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
    else:
        print(f"Artist '{artist_name_input}' not found.")

# !------- Task 5: Get Released Albums By Year by Salah -------!
def get_released_albums_by_year():
    year = input("Please enter a year: ").strip()
    if not year.isdigit():
        print("Invalid year. Please enter a numeric value.")
        return

    albums_found = []

    for filename in os.listdir(ALBUMS_DIR):
        if filename.endswith(".json"):
            album_path = os.path.join(ALBUMS_DIR, filename)
            album_data = load_json(album_path)

            for album in album_data.get("items", []):
                release_date = album.get("release_date", "")
                if release_date.startswith(year):
                    album_name = album.get("name", "Unknown Album")
                    artists = album.get("artists", [])

                    artist_name = ", ".join(
                        artist.get("name", "Unknown Artist").strip()
                        for artist in artists
                    )

                    albums_found.append((album_name, artist_name))

    if not albums_found:
        print(f"No albums were released in the year {year}.")
        return

    albums_found.sort()
    print(f"Albums released in the year {year}:")
    for album_name, artist_name in albums_found:
        print(f'- "{album_name}" by {artist_name}.')

# !------- Task 6: Analyze Song Lyrics by Ali -------!
def moosify_lyrics():
    lyrics = search_songs_by_keyword()

    if not lyrics:
            print("Lyrics not found")
            
    if not re.search(r'mo|\!|\?', lyrics, re.IGNORECASE):
            title = ().get("title", "Unknown")
            artist = ().get("artist", "")
            song_info = f"{title} by {artist}" if artist else title
            print(f"{song_info} is not moose-compatible!")

            moosified = re.sub(r'\b\w*mo\w*\b', "moo", lyrics, flags=re.IGNORECASE)
            moosified = re.sub(r'[!?]', "moo", moosified)

            title = ().get("title", "Unknown")
            filename = f"{title} Moosified.txt"
            os.makedirs(MOOSIFIED_DIR, exist_ok=True)
            filepath = os.path.join(MOOSIFIED_DIR, filename)

            try:
                with open(filepath, "w", encoding="utf-8") as file:
                    file.write(moosified)
            except IOError:
                print(f"Error: Could not write to file - {filepath}")

            artist = ().get("artist", "")
            song_info = f"{title} by {artist}" if artist else title

# !------- Task 7: Calculate Longest Unique Word Sequence In A Song by Ifty -------!
def process_text_for_analysis(text):
    text = re.sub(r'\s+', ' ', text)
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    words = text.split(" ")
    processed_words = []
    for word in words:
        if word:
            processed_words.append(word)
    return processed_words

def calculate_longest_unique_sequence():
    songs = get_available_songs()

    if not songs:
        print("No songs available.")
        return

    print("Available songs:")
    index = 0
    for song in songs:
        artist = song.get("artist") or "Unknown"
        print(f"{index + 1}. {song.get('title')} by {artist}")
        index += 1

    choice = input("Please select one of the following songs (number): ").strip()
    if choice.isdigit():
        choice = int(choice)
        if choice < 1 or choice > len(songs):
            print("Invalid choice.")
            return

        entry = songs[choice - 1]
        lyrics = search_songs_by_keyword(entry)

        if lyrics:
            words = process_text_for_analysis(lyrics)

            if words:
                seen = {}
                start = 0
                max_len = 0
                end = 0
                for word in words:
                    if word in seen and seen[word] >= start:
                        start = seen[word] + 1
                    seen[word] = end
                    max_len = max(max_len, end - start + 1)
                    end += 1

                print(f"The length of the longest unique sequence in {entry.get('title')} is {max_len}")
            else:
                print("No valid words found in the lyrics.")
        else:
            print("No lyrics found for this song.")
    else:
        print("Invalid choice.")

# !------- Task 8: Weather Forecast For Upcoming Concerts by Salah -------!
WEATHER_FIELDS = [
    "precipitation", "date", "city", "city_code",
    "temperature_avg", "temperature_max", "temperature_min",
    "wind_direction", "wind_speed"
]

def read_concert_data():
    concerts = []
    artists = set()

    if not os.path.isfile(CONCERTS_CSV):
        print("Error: 'concerts.csv' file is missing.")
        return concerts, sorted(artists)

    try:
        with open(CONCERTS_CSV, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                artist = (row.get("artist") or "").strip()
                city_code = (row.get("city_code") or "").strip()
                month = row.get("month", "").strip()
                day = row.get("day", "").strip()
                year = row.get("year", "").strip()

                if not all([artist, city_code, month, day, year]):
                    continue
                if not (month.isdigit() and day.isdigit() and year.isdigit()):
                    continue

                date = f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
                concerts.append({"artist": artist, "city_code": city_code, "date": date})
                artists.add(artist)
    except (IOError, csv.Error) as e:
        print(f"Error reading concerts CSV: {e}")

    return concerts, sorted(artists)

def read_weather_data():
    weather_lookup = {}

    if not os.path.isfile(WEATHER_CSV):
        print("Error: 'weather.csv' file is missing.")
        return weather_lookup

    try:
        with open(WEATHER_CSV, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                city_code = (row.get("city_code") or "").strip()
                date = (row.get("date") or "").strip()

                if city_code and date:
                    key = (city_code, date)
                    weather_lookup[key] = {
                        field: (row.get(field) or "").strip()
                        for field in WEATHER_FIELDS
                    }
    except (IOError, csv.Error) as e:
        print(f"Error reading weather CSV: {e}")

    return weather_lookup

def format_date(date_string):
    date_obj = datetime.strptime(date_string, "%Y-%m-%d")
    day = date_obj.day
    month = date_obj.strftime("%B")
    year = date_obj.year

    if day in [1, 21, 31]:
        suffix = "st"
    elif day in [2, 22]:
        suffix = "nd"
    elif day in [3, 23]:
        suffix = "rd"
    else:
        suffix = "th"

    return f"{month} {day}{suffix} {year}"

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

def predict_weather_for_concerts():
    concerts, artist_list = read_concert_data()
    weather_data = read_weather_data()

    if not concerts:
        print("No upcoming concerts found.")
        return

    print("Upcoming artists:")
    for artist in artist_list:
        print(f"- {artist}")

    artist_input = input("Please input the name of one of the following artists: ").strip()

    matching_concerts = []
    
    for concert in concerts:
        if concert["artist"].lower() == artist_input.lower():
            matching_concerts.append(concert)

    if not matching_concerts:
        print(f"No upcoming concerts found for '{artist_input}'.")
        return

    formatted_artist = next((a for a in artist_list if a.lower() == artist_input.lower()), artist_input)

    print(f'Fetching weather forecast for "{formatted_artist}" concerts...')
    
    if len(matching_concerts) == 1:
        concert_word = "concert"
    else:
        concert_word = "concerts"

    print(f"{formatted_artist} has {len(matching_concerts)} upcoming {concert_word}:")

    for concert in matching_concerts:
        key = (concert["city_code"], concert["date"])
        weather = weather_data.get(key)

        if weather:
            city = weather.get("city", "Unknown City")
            formatted_date = format_date(concert["date"])
            message = forecast_message(weather)
            print(f"- {city}, {formatted_date}. {message}")
        else:
            print(f"- {concert['city_code']}, {concert['date']}. Weather data not available.")

# !------- Task 9: Search Song By Lyrics by Ifty -------!
def build_inverted_index():
    inverted_index = {}
    
    try:
        files = os.listdir(SONGS_DIR)
    except FileNotFoundError:
        print(f"Error: Songs directory not found - {SONGS_DIR}")
        return inverted_index
    
    for file in files:
        if file.endswith(".json"):
            song_path = os.path.join(SONGS_DIR, file)
            song_data = load_json(song_path)
            
            if song_data:
                title = song_data.get("name", "") or song_data.get("title", "")
                lyrics = song_data.get("lyrics", "")
                
                if lyrics and title:
                    words = process_text_for_analysis(lyrics)
                    
                    for word in words:
                        if word not in inverted_index:
                            inverted_index[word] = []
                        if title not in inverted_index[word]:
                            inverted_index[word].append(title)
    
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
    except IOError as e:
        print(f"Warning: Could not save inverted index: {e}")
    
    return inverted_index

def search_by_lyrics():
    query = input("Please type the lyrics you'd like to search for: ").strip()
    
    if query:
        query_words = process_text_for_analysis(query)
        
        if query_words:
            inverted_index = load_or_create_inverted_index()
            
            song_scores = {}
            
            for word in query_words:
                if word in inverted_index:
                    for song in inverted_index[word]:
                        if song not in song_scores:
                            song_scores[song] = 0
                        song_scores[song] += 1
            
            if song_scores:
                sorted_songs = sorted(song_scores.items(), key=lambda x: x[1], reverse=True)
                
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