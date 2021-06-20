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
1- Wrote all SQL queries regarding drop and creation of all tables, and revised the script in create_tables.py Running this script will create a clean resetted version of the tables.   
2- Started the ETL process, with etl.ipynb, using python, which calls for postgreSQL functions written in sql_queries.py.  
3- Completed the script in etl.py, which reads the datasets and populates the tables.    
4- During the process test.ipynb was used to read what has been written in the tables, to keep track of the progress.  

## How to run the scripts: 
In order to run this project locally you will have to:   
1- Create a postgreSQL server. You can find the installation files [here](https://www.postgresql.org/download/).  
2- From the installation, you will define a username and password to your server. To securely store them, create a file called credentials.py where you should declare two variables like this:  
```python
user = "user_example"
password = "password_example"
```
It's important to include this script in your .gitignore file, this way your password won't be uploaded to github in the case you publish the project. This script will be called by the functions to retrieve the server's username and password.  
3- Run your scripts from your terminal. **Careful** make sure you don't have a database already called sparkifydb, as this script will drop and create a new one, as well as the tables in it:  
	* First to create the database:   
	```
	$ python3 create_tables.py
	```  
	* Then to fill the tables:  
	```
	$ python3 etl.py
	```  
	If all went well, you will see printed that all files were loaded in the tables.   	
4- To test if the data has been properly inserted, you can run the jupyter notebook test.ipynb, and look into what has been inserted in the tables.   


## To do / to be improved:
-Make a diagram of the database for this readme file.  
-Test this project with a bigger database, and not a sample of it.



