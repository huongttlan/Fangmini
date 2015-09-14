###################################################
#  Anaylize data from csv formatted files
#  Fro SQL miniproject
###################################################
import sqlite3, csv
import numpy as np
from scipy import stats
import pandas as pd

# connect to the database
conn = sqlite3.connect('sql_fang.db')
conn.text_factory = str
c = conn.cursor()

###################### score by zipcode ###################
# standard error function, using splite aggregation function
class ScipySEMAggregate(object):
    def __init__(self):
        self.values = []
    def step(self, value):
        #print self.values
        if value != '':
            self.values.append(float(value))
    def finalize(self):
        return stats.sem(self.values)
conn.create_aggregate("sp_sem", 1, ScipySEMAggregate)


# creat new table, select zipcode and score from WebExtract_f
c.execute("DROP TABLE IF EXISTS A;")
c.execute('''CREATE TABLE A AS SELECT ZIPCODE, SCORE FROM WebExtract_f
                ;''')

# creat new table, score by zipcode
c.execute("DROP TABLE IF EXISTS B;")
c.execute('''CREATE TABLE B AS SELECT ZIPCODE, AVG(SCORE) AS MEANGRADE, 
                    sp_sem(SCORE) AS SEM, COUNT(*) AS NUM_INSP FROM WebExtract_f
                    GROUP BY ZIPCODE
                    ;''')

# creat new table, filter by number of inspection > 100
c.execute("DROP TABLE IF EXISTS C;")
c.execute('''CREATE TABLE C AS SELECT * FROM B
                WHERE NUM_INSP>100
                ;''')
c.execute('''SELECT * FROM C
                    ;''')
a = c.fetchall()
print len(a)
print a

###################### score_by_borough ###################
# creat BOROUGH table
c.execute("DROP TABLE IF EXISTS BOROUGH;")
c.execute('''CREATE TABLE BOROUGH AS SELECT BORO, AVG(SCORE) AS MEANGRADE, 
                    sp_sem(SCORE) AS SEM, COUNT(*) AS NUM_INSP FROM WebExtract_f
                    GROUP BY BORO
                    ;''')

# update boro code with boro name
c.execute('''UPDATE BOROUGH
                    SET BORO='MANHATTAN'
                    WHERE BORO='1'
                    ;''')
c.execute('''UPDATE BOROUGH
                    SET BORO='THE BRONX'
                    WHERE BORO='2'
                    ;''')
c.execute('''UPDATE BOROUGH
                    SET BORO='BROOKLYN'
                    WHERE BORO='3'
                    ;''')
c.execute('''UPDATE BOROUGH
                    SET BORO='QUEENS'
                    WHERE BORO='4'
                    ;''')
c.execute('''UPDATE BOROUGH
                    SET BORO='STATEN ISLAND'
                    WHERE BORO='5'
                    ;''')
# order boroughs by grade
c.execute('''SELECT * FROM BOROUGH
             WHERE BORO>0
             ORDER BY MEANGRADE
                    ;''')
a = c.fetchall()
print a

###################### score_by_cuisine ###################
# creat CUISINE table
c.execute("DROP TABLE IF EXISTS CUISINE;")
c.execute('''CREATE TABLE CUISINE AS SELECT CUISINECODE, AVG(SCORE) AS MEANGRADE, 
                    sp_sem(SCORE) AS SEM, COUNT(*) AS NUM_INSP FROM WebExtract_f
                    GROUP BY CUISINECODE
                    ;''')
c.execute("DROP TABLE IF EXISTS CUISINE2;")

# joint with CUISINE_f to get the CUISINE discription
c.execute('''CREATE TABLE CUISINE2 AS SELECT CUISINE.*, CUISINE_f.CODEDESC
                FROM CUISINE
                LEFT JOIN CUISINE_f
                ON CUISINE.CUISINECODE=CUISINE_f.CUISINECODE
                ;''')
# filter by number of inspection > 100
c.execute('''SELECT CUISINECODE, MEANGRADE, SEM, NUM_INSP FROM CUISINE2
             WHERE NUM_INSP>100
             ORDER BY MEANGRADE
                    ;''')
a = c.fetchall()
print len(a)

###################### violation_by_cuisine ###################
# VIO_TABLE: create table of violationcode and violationdesc
c.execute("DROP TABLE IF EXISTS VIO_TABLE;")
c.execute('''CREATE TABLE VIO_TABLE AS SELECT VIOLATIONCODE, VIOLATIONDESC FROM VIOLATION_f
                    WHERE CAST(ENDDATE AS DATE)>CAST('2014-01-01 00:00:00' AS DATE)
                    ;''')

# VIO_CUI_INSTANCE_TABLE create table of violationcode and cuisinecode 
c.execute("DROP TABLE IF EXISTS VIO_CUI_INSTANCE_TABLE;")
c.execute('''CREATE TABLE VIO_CUI_INSTANCE_TABLE AS SELECT VIOLCODE, CUISINECODE FROM WebExtract_f
                    ;''')

#Calculate unconditional probability
c.execute('''SELECT COUNT(*) FROM WebExtract_f''')
a = c.fetchall()[0]
N = a[0] # total violation number
print N # N=531935

# VIO_UNCOND_TABLE: create table of violation uncond probability and violationcode 
c.execute("DROP TABLE IF EXISTS VIO_UNCOND_TABLE;")
c.execute('''CREATE TABLE VIO_UNCOND_TABLE AS 
            SELECT COUNT(*)*1.0/531935 AS CNT, VIOLCODE FROM WebExtract_f
                GROUP BY VIOLCODE
                    ;''')

# GRP_VIO_CUI_TABLE: create table and group by violcode and cuisinecode, from VIO_CUI_INSTANCE_TABLE
c.execute("DROP TABLE IF EXISTS GRP_VIO_CUI_TABLE;")
c.execute('''CREATE TABLE GRP_VIO_CUI_TABLE AS  Select CUISINECODE, VIOLCODE, Count(*) As Count1
                From   VIO_CUI_INSTANCE_TABLE
                Group By CUISINECODE, VIOLCODE
                ;''')
# GRP_VIO_CUI_TABLE_100: filter by Count1 > 100
c.execute("DROP TABLE IF EXISTS GRP_VIO_CUI_TABLE_100;")
c.execute('''CREATE TABLE GRP_VIO_CUI_TABLE_100 AS SELECT * FROM GRP_VIO_CUI_TABLE
             WHERE Count1>100
                    ;''')

# VIO_COND_CUI_TABLE: Calculate conditional probability
c.execute("DROP TABLE IF EXISTS VIO_COND_CUI_TABLE;")
c.execute('''CREATE TABLE VIO_COND_CUI_TABLE AS Select A.VIOLCODE, A.CUISINECODE, A.Count1 * 1.0 / B.Count2 As Freq, A.Count1
             From GRP_VIO_CUI_TABLE_100 As A
        Inner Join (
                Select CUISINECODE, Count(*) As Count2
                From   VIO_CUI_INSTANCE_TABLE
                Group By CUISINECODE
                ) As B
                On A.CUISINECODE = B.CUISINECODE
                ORDER BY Freq DESC
                ;''')

# Calculate the ratio, and join tables to add descriptions
c.execute("DROP TABLE IF EXISTS RATIO_TABLE;")
c.execute('''CREATE TABLE RATIO_TABLE AS SELECT VIO_COND_CUI_TABLE.Freq*1.0/VIO_UNCOND_TABLE.CNT AS Prob, * FROM VIO_COND_CUI_TABLE
                LEFT JOIN VIO_UNCOND_TABLE
                ON VIO_COND_CUI_TABLE.VIOLCODE=VIO_UNCOND_TABLE.VIOLCODE
                ORDER BY PROB DESC
                ;''')

c.execute("DROP TABLE IF EXISTS RATIO_TABLE_final;")
c.execute('''CREATE TABLE RATIO_TABLE_final AS SELECT A.*, VIO_TABLE.VIOLATIONDESC AS VIOlationdesc FROM 
                (SELECT RATIO_TABLE.*, CUISINE_f.CODEDESC
                FROM RATIO_TABLE
                LEFT JOIN CUISINE_f
                ON RATIO_TABLE.CUISINECODE=CUISINE_f.CUISINECODE) AS A
                LEFT JOIN VIO_TABLE
                ON A.VIOLCODE=VIO_TABLE.VIOLATIONCODE
                ;''')
c.execute('''SELECT CODEDESC, VIOLATIONDESC, PROB, Count1 FROM RATIO_TABLE_final;''')
a = c.fetchall()
a[1:21]
lt = [((k[0], k[1]), k[2], k[3]) for k in a[1:21]]
lt
