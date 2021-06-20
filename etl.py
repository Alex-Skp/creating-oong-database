import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
from credentials import user, password


def process_song_file(cur, filepath):
    """
    This function reads the song json file from the filepath
    and inserts the record in the song and artist tables. 
    Arguments:
        cur: cursor object for the database connection.
        filepath: json song file path as a string.
    """
    # open song file
    df = pd.read_json(filepath, typ='series')

    # insert song record
    song_data = list(df[['song_id','title','artist_id','year','duration']].values)
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = list(df[['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']].values)
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    This function will process the log files:
    - timestamps are converted and inserted in the time table.
    - user data is gathered and inserted in user table.
    - songplays are queried in the song and artist tables to retrieve both IDs;
      If no matches are found it will write None, then the data is inserted in songplay table.
    Arguments:
        cur: cursor object for the database connection.
        filepath: json log file path as a string.
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page']=='NextSong']

    # convert timestamp column to datetime
    df['ts'] = pd.to_datetime(df['ts'], unit='ms', origin='unix')
    t = pd.concat([df['ts'], 
               df['ts'].dt.hour,
               df['ts'].dt.day,
               df['ts'].dt.week, 
               df['ts'].dt.month,
               df['ts'].dt.year,
               df['ts'].dt.weekday], axis=1)
    t.columns = ['timestamp','hour','day','week','month','year','weekday']
    
    # insert time data records
    time_df = t

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = [row.ts,
                         row.userId,
                         row.level,
                         songid,
                         artistid,
                         row.userId,
                         row.location,
                         row.userAgent]
        cur.execute(songplay_table_insert, list(songplay_data))


def process_data(cur, conn, filepath, func):
    """
    This function walks through all folders in the filepath, and applies the function passed as func, in order to write the data in the databases pointed by the cursor. 
    Arguments:
        cur: cursor object.
        conn: connection to the database.
        filepath: location of data file path where json files are located, as a string.
        func: function that transforms data and inserts it in the database
        
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    Connects to the database, sets the cursor and executes the data extraction, transformation, and load.
    closes the connection in the end.
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user={} password={}".format(user,password))
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()