###################################################
#  Load data from csv formatted files
#  Fro SQL miniproject
###################################################
import sqlite3, csv
import numpy as np
from scipy import stats

# connect
conn = sqlite3.connect('sql_fang.db')
c = conn.cursor()

##########################
# Create table action_f
c.execute("DROP TABLE IF EXISTS action_f;")
c.execute('''CREATE TABLE action_f
             (STARTDATE Datetime, ENDDATE Datetime, ACTIONCODE nchar(10), ACTIONDESC nvarchar(150))''')

with open('Action.txt', 'rt') as f:
    dr = csv.DictReader(f)
    to_db = [(i['STARTDATE'],i['ENDDATE'],i['ACTIONCODE'], i['ACTIONDESC']) for i in dr]
    print to_db[0]
    
conn.executemany("INSERT INTO action_f (STARTDATE, ENDDATE, ACTIONCODE, ACTIONDESC) VALUES (?, ?, ?, ?);", to_db)



##########################
# Create table  cuisine_f
c.execute("DROP TABLE IF EXISTS cuisine_f;")
c.execute('''CREATE TABLE cuisine_f(CUISINECODE Nchar(10), CODEDESC Varchar(200))''')

with open('Cuisine.txt', 'rt') as f:
    dr = csv.DictReader(f)
    to_db = [(i['CUISINECODE'],i['CODEDESC']) for i in dr]
    print to_db[35]
    
conn.executemany("INSERT INTO Cuisine_f (CUISINECODE, CODEDESC) VALUES (?, ?);", to_db)


##########################
# Create table  Violation_f
c.execute("DROP TABLE IF EXISTS Violation_f;")
c.execute('''CREATE TABLE Violation_f(STARTDATE Datetime, ENDDATE Datetime, VIOLATIONCODE nchar(3), VIOLATIONDESC nvarchar(600), CRITICALFLAG nchar(1))''')

with open('Violation.txt', 'rt') as f:
    dr = csv.DictReader(f)
    to_db = [(i['STARTDATE'],i['ENDDATE'], i['VIOLATIONCODE'], i['VIOLATIONDESC'], i['CRITICALFLAG']) for i in dr]
    print to_db[35]
    
conn.executemany("INSERT INTO Violation_f (STARTDATE, ENDDATE, VIOLATIONCODE, VIOLATIONDESC, CRITICALFLAG) VALUES (?, ?, ?, ?, ?);", to_db)




##########################
# Create table WebExtract_f 
c.execute("DROP TABLE IF EXISTS WebExtract_f;")
c.execute('''CREATE TABLE WebExtract_f( CAMIS Varchar(10),
                                        DBA varchar(255),
                                        BORO Varchar(1),
                                        BUILDING Varchar(10),
                                        STREET Varchar(100),
                                        ZIPCODE Varchar(5),
                                        PHONE Varchar(20),
                                        CUISINECODE Varchar(2),
                                        INSPDATE Datetime,
                                        ACTION Varchar(1),
                                        VIOLCODE Varchar(3),
                                        SCORE Varchar(3),
                                        CURRENTGRADE Varchar(1),
                                        GRADEDATE Datetime,
                                        RECORDDATE Datetime)''')

with open('WebExtract.txt', 'rt') as f:
    dr = csv.DictReader(f)
    to_db = [(i['CAMIS'],
              i['DBA'], 
              i['BORO'], 
              i['BUILDING'], 
              i['STREET'],
              i['ZIPCODE'], 
              i['PHONE'], 
              i['CUISINECODE'], 
              i['INSPDATE'], 
              i['ACTION'], 
              i['VIOLCODE'],
              i['SCORE'],
              i['CURRENTGRADE'],
              i['GRADEDATE'],
              i['RECORDDATE']) for i in dr]
    print to_db[0:10]

conn.executemany('''INSERT INTO WebExtract_f (CAMIS,
                                        DBA,
                                        BORO,
                                        BUILDING,
                                        STREET,
                                        ZIPCODE,
                                        PHONE,
                                        CUISINECODE,
                                        INSPDATE,
                                        ACTION,
                                        VIOLCODE,
                                        SCORE,
                                        CURRENTGRADE,
                                        GRADEDATE,
                                        RECORDDATE) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''', to_db)
resoverall = c.execute("SELECT * FROM WebExtract_f;")


    

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()







