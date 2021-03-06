import psycopg2
import pandas as pd

# Load data
data = pd.read_csv(
    "/mnt/c/Users/William's Zenbook/Desktop/Data Science (4142)/COVID-Tracking-Data-Mart/Data/Date/Reported_Date_dimension.csv")

# Connect to database
conn = psycopg2.connect(
    "host=www.eecs.uottawa.ca port=15432 dbname=group_20 user=whuyn056 password=")

# Open a cursor to perform database operations
cur = conn.cursor()

# Create table
cur.execute("""DROP TABLE if exists d_reported_date;
            CREATE TABLE d_reported_date
            (
            reported_date_surrogate_key    INT NOT NULL,
            reported_date_key              INT NOT NULL,
            day                         INT NOT NULL,
            month                       INT NOT NULL,
            day_of_week                 VARCHAR(10),
            day_of_week_num             INT,
            week_in_year                INT,
            holiday                     BOOLEAN,
            season                      VARCHAR(10),
            weekend                     BOOLEAN,
            year                        INT NOT NULL,
            date_full_format            DATE,
            PRIMARY KEY (reported_date_surrogate_key)
            );""")

# Insert values from data to table
sqlInsert = """ INSERT INTO d_reported_date (reported_date_surrogate_key, reported_date_key, day, month, day_of_week, day_of_week_num,
    week_in_year, holiday,season, weekend, year, date_full_format) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
for idx, row in data.iterrows():
    record = (row["Reported_Date_Surrogate_Key"], row["Reported_Date_Key"], row["Day"], row["Month"],
              row["Day_of_Week_Name"], row["Day_of_Week_Num"], row["Week_in_Year"],  row["Holiday"],
              row["Season"], row["Weekend"], row["Year"], row["Date_Full_Format"])
    cur.execute(sqlInsert, record)

# Make the changes to the database persistent
conn.commit()

# Close connections
cur.close()
conn.close()
