Assignment 2: Mooziq
====================

Authors: Ifty Zubaer and Salah Alabdullah  
Group: Ifty Salah Ali  
Course: DIT009 – Fundamentals of Programming

---

Task Division
-------------
- Task 0: **Ifty** implemented the Project Setup / Helper Utilities.
- Task 0.1: **Ifty** implemented the Main menu.
- Task 1: **Ifty**  implemented the Get All Artists.
- Task 2: **Ifty** implemented the Get All Albums By An Artist.
- Task 3: **Ifty** implemented the Get Top Tracks By An Artist. 
- Task 4: **Ifty** implemented the Export Artist Data.  
- Task 5: **Salah** implemented the Get Released Albums By Year.
- Task 6: **Ifty** implemented the Song Creativity Score (Moosify Lyrics).
- Task 7: **Ifty** implemented the Calculate Longest Unique Word Sequence in a Song.
- Task 8: **Salah** implemented the Weather Forecast For Upcoming Concerts.
- Task 9: **Ifty** implemented the Search Song By Lyrics (Inverted Index).
- Each member implemented the error handling for their own tasks.  
- Code Review / Project Review: **Ifty** also acted as the reviewer for the project. This also included helping group members debug and improve their tasks when needed, to ensure that the entire project was consistent and working correctly.

---

Project Description
-------------------
Mooziq is a music analysis and discovery platform designed as part of the DIT009 course. 
It allows users to retrieve and analyze data about artists, albums, tracks, song lyrics, and upcoming concerts using a structured dataset of JSON and CSV files.

The program features:
- A main menu with numbered options.
- Tasks for querying and exporting artist data.
- Song lyric processing and analysis.
- Weather forecast analysis for upcoming concerts.
- A basic search engine to find songs based on lyrics.

All outputs strictly follow the required printing templates so they can be validated by CodeGrade.

---

How to Run
----------
1. Make sure the folder structure matches the required template:
   ```
   .
   ├── main.py
   └── dataset
       ├── albums
       ├── artists
       ├── concerts
       ├── songs
       ├── top_tracks
       └── weather
   ```

2. Run the program:
   ```
   python main.py
   ```

3. The main menu will appear:
   ```
   Welcome to Mooziq!
   Choose one of the options below:

   1. Get All Artists
   2. Get All Albums By An Artist
   3. Get Top Tracks By An Artist
   4. Export Artist Data
   5. Get Released Albums By Year
   6. Analyze Song Lyrics
   7. Calculate Longest Unique Word Sequence In A Song
   8. Weather Forecast For Upcoming Concerts
   9. Search Song By Lyrics
   10. Exit

   Type your option:
   ```

4. Type the option number to use each feature.  
5. Option 10 ends the program gracefully.

---

Example Usage
-------------
Below are examples based on the assignment description:

Task 1: Get All Artists
-----------------------
Input
```
Type your option: 1
```
Output
```
Artists found in the database:
- MASS OF THE FERMENTING DREGS
- Pierce The Veil
- Sleeping With Sirens
```

Task 2: Get All Albums By An Artist
-----------------------------------
Input
```
Type your option: 2
```
Output
```
Artists found in the database:
- MASS OF THE FERMENTING DREGS
- Pierce The Veil
- Sleeping With Sirens
```
Input
```
Please input the name of an artist: Sleeping With Sirens
```
Output
```
Listing all available albums from Sleeping With Sirens…
- “Complete Collapse (Deluxe)” was released in September 29th 2023
- “Complete Collapse” was released in October 14th 2022
- “How It Feels to Be Lost (Deluxe)” was released in September 6th 2019
- “How It Feels to Be Lost” was released in September 6th 2019
- “Gossip” was released in September 22nd 2017
- “Live and Unplugged” was released in April 8th 2016
- "Madness (Deluxe Edition)" was released in March 17th 2015
- "Feel" was released in May 31st 2013
```

Task 3: Get Top Tracks By An Artist
------------------------------------
Input
```
Type your option: 3
```
Output
```
Artists found in the database:
- MASS OF THE FERMENTING DREGS
- Pierce The Veil
- Sleeping With Sirens
```
Input
```
Please input the name of an artist: Sleeping With Sirens
```
Output
```
Listing top tracks for Sleeping With Sirens…
- "If You Can't Hang” has a popularity score of 72. It is made for the charts!
- “If I'm James Dean, You're Audrey Hepburn” has a popularity score of 68. It is quite popular now!
- “A Trophy Fathers Trophy Son” has a popularity score of 66. It is quite popular now!
- “The Bomb Dot Com V2.0” has a popularity score of 65. It is quite popular now!
- “Do It Now, Remember It Later” has a popularity score of 35. Popular song.
- “Better Off Dead” has a popularity score of 61. It is quite popular now!
```

Task 4: Export Artist Data
--------------------------
**Artist does not exist in the csv file:**  
Input
```
Type your option: 4
```
Output
```
Artists found in the database:
- MASS OF THE FERMENTING DREGS
- Pierce The Veil
- Sleeping With Sirens
```
Input
```
Please input the name of an artist: Sleeping With Sirens
```
Ouput
```
Exporting 'Sleeping With Sirens' data to artist-data.csv...
Data successfully added!
```

**Artist already exists in the csv file:**  
Input
```
Type your option: 4
```
Output
```
Artists found in the database:
- MASS OF THE FERMENTING DREGS
- Pierce The Veil
- Sleeping With Sirens
```
Input
```
Please input the name of an artist: Sleeping With Sirens
```
Output
```
Exporting 'Sleeping With Sirens' data to artist-data.csv...
Data successfully updated!
```

Task 5:  Get Released Albums By Year
------------------------------------
Input
```
Type your option: 5
Please enter a year: 2022
```
Output
```
Albums released in the year: 2022
- "Awakening:Sleeping" by MASS OF THE FERMENTING DREGS
- "Complete Collapse" by Sleeping With Sirens
- "Complete Collapse (Acoustic)" by Sleeping With Sirens
- "Complete Collapse" by Sleeping With Sirens
- "Complete Collapse" by Sleeping With Sirens
- "Crosses (feat. Spencer Chamberlain of Underoath)" by Sleeping With Sirens
- "Let You Down (feat. Charlotte Sands)" by Sleeping With Sirens
- "Let You Down (feat. Charlotte Sands)" by Sleeping With Sirens
- "MESS (with Kellin Quinn of Sleeping With Sirens)" by Sleeping With Sirens
- "worm food" by Pierce The Veil
```

Task 6: Song Creativity Score
-----------------------------
Input
```
Type your option: 6
```
Output
```
Available songs:
0. Bulls In The Bronx by Pierce The Veil
1. Mr. Blue Sky by Electric Light Orchestra
2. So Long by ABBA
3. My Queen (feat. Spiritbox) by Babymetal
4. Yellowjacket - feat. Sam Carter by Spiritbox
```

**Cannot be moos-ified:**  
Input
```
Please select one of the following songs (number): 1
```
Output
```
Bulls In The Bronx by Pierce The Veil is not moose-compatible!
```

**Can be moos-ified:**  
Input
```
Please select one of the following songs (number): 2
```
Output
```
Mr. Blue Sky by Electric Light Orchestra has been moos-ified!
File saved at ./moosified/Electric Light Orchestra Moosified.txt
 ___            ___
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
```

Task 7: Calculate Longest Unique Word Sequence In A Song
--------------------------------------------------------
Input
```
Type your option: 7
```
Output
```
Available songs:
0. Bulls In The Bronx by Pierce The Veil
1. Mr. Blue Sky by Electric Light Orchestra
2. So Long by ABBA
3. My Queen (feat. Spiritbox) by Babymetal
4. Yellowjacket - feat. Sam Carter by Spiritbox
```
Input
```
Please select one of the following songs (number): 0
```
Output
```
The length of the longest unique word sequence in Bulls In The Bronx is 8
```

Task 8: Get Forecast For Upcoming Concerts
------------------------------------------
Input
```
Type your option: 8
```
Output
```
Upcoming artists:
- Sleeping With Sirens
- Pierce The Veil
- MASS OF THE FERMENTING DREGS
```
Input
```
Please input the name of one of the following artists: Pierce The Veil
```
Output
```
Fetching weather forecast for 'Pierce The Veil' concerts...
Pierce The Veil has 2 upcoming concerts:
- Gothenburg, September 22nd 2025. Wear warm clothes. Bring an umbrella.
- New York, September 26th 2025. Perfect weather!
- Copenhagen, October 2nd 2025. Bring a raincoat.
- Berlin, October 21st 2025. Bring water. Bring an umbrella.
```

Task 9: Search Song By Lyrics
-----------------------------
Input
```
Type your option: 9
Please type the lyrics you'd like to search for: For So long
```
Output
```
Listing matches for 'for so long'...
- Mr. Blue Sky with a score of 3
- So Long with a score of 2
```

---

Grading Goals
-------------
- Grade 3 (Pass): Tasks 1–7 implemented.
- Grade 4 (Pass with Merit): Task 8 implemented.
- Grade 5 (Pass with Distinction): Tasks 8 and 9 implemented.

This submission includes Tasks 1–8 and full error handling (Task 9), therefore targeting **Grade 5 (Distinction)**.