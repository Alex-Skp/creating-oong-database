HEAD
# Data Modelling with postgres
## Case Study:
**Creating a database for Sparkify**
The objective is to create a relational database using PostgreSQL based in two datasets:
* Songs:
We have a subset from which we will extract information about songs and their artists.
In the future when running this project locally, we'll bring on a bigger subset, as in this case we found that several artists or songs were not found, and our songplays table has too many nulls in artist and song IDs. 
* Log:
We will extract user play interactions, to create the database, and store a clean version of this data for future analysis.

### Target Schema:
* Fact Table
    * songplays - records in log data associated with song plays i.e. records with page NextSong 
    columns: songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
* Dimension Tables
    * users - users in the app
    user_id, first_name, last_name, gender, level
    * songs - songs in music database
    song_id, title, artist_id, year, duration
    * artists - artists in music database
    artist_id, name, location, latitude, longitude
    * time - timestamps of records in songplays broken down into specific units
    start_time, hour, day, week, month, year, weekday

## Steps taken:
1.- Wrote all SQL queries regarding drop and creation of all tables, and revised the script in create_tables.py Running this script will create a clean resetted version of the tables. 
2.- Started the ETL process, with etl.ipynb, using python, which calls for postgreSQL functions written in sql_queries.py
3.- Completed the script in etl.py, which reads the datasets and populates the tables.
4.- During the process test.ipynb was used to read what has been written in the tables, to keep track of the progress.

## To do / to be improved:
-Make a diagram of the database for this readme file.
-Revise the queries which extract the ID information for the songplays table, as a lot of None values are returned. Maybe a bigger song database is needed, or a better matching search logic is needed. 
-Run a local version of this project, and upload in my personal GitHub 