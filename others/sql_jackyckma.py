# -*- coding: utf-8 -*-
#import fellow
#import typecheck


'''
(zipcode, mean grade, standard error, number of inspections)
typecheck.returns("184 * (string, number, number, count)")
'''
def score_by_zipcode():
    c = con.cursor()
    k= c.execute('SELECT ZIPCODE, AVG(SCORE) as MEAN_GRADE, stderr(SCORE), count(SCORE) FROM grades GROUP BY ZIPCODE HAVING count(*)>=100 ORDER BY MEAN_GRADE')
    return k.fetchall()
    #return [("11201", 21.9060928719313812, 0.179441607823702, 6762)] * 184

#typecheck.returns("string")
def score_by_map():
    # must be url starting with ctb.io
    return "http://cdb.io/1O5tIy4"


'''
(borough, mean grade, stderr, number of inspections)
typecheck.returns("5 * (string, number, number, count)")
'''
def score_by_borough():
    c = con.cursor()
    k= c.execute('SELECT boroname, AVG(SCORE) as MEAN_GRADE, stderr(SCORE), count(SCORE) FROM grades join boroughs on grades.boro = boroughs.boro GROUP BY grades.boro ORDER BY MEAN_GRADE')
    return k.fetchall()
    #return [("MANHATTAN", 22.2375933589636849, 0.0332739265922062, 204185)] * 5

'''
(cuisine, mean grade, stderr, number of inspections)
typecheck.returns("75 * (string, number, number, count)")
'''
def score_by_cuisine():
    c = con.cursor()
    sqlquery="""SELECT codedesc, AVG(SCORE) as MEAN_GRADE, stderr(SCORE), count(*) as Count 
            FROM grades 
            INNER JOIN(
                SELECT grades.cuisinecode, codedesc, count(*) as Count 
                FROM grades JOIN cuisines 
                ON grades.cuisinecode = cuisines.cuisinecode 
                GROUP BY grades.cuisinecode 
                HAVING Count>=100 
            ) AS c ON c.CUISINECODE=grades.CUISINECODE
            GROUP BY grades.cuisinecode 
            ORDER BY MEAN_GRADE"""
    k= c.execute(sqlquery)
    return k.fetchall()    
    #return [("French", 21.9985734664764622, 0.177094690841052, 7010)] * 75

'''
((cuisine, violation), ratio, count)
typecheck.returns("20 * ((string, string), number, count)")
'''
def violation_by_cuisine():
    c = con.cursor()
    sqlquery="""Select CodeDesc, ViolationDesc, (cast(InspCount as float) * TotalCount / ViolCount / CuiCount) as Ratio, InspCount 
            From(
            	Select cuisinecode, violcode, Count(*) As InspCount
            	From grades
            	Where cuisinecode is not null and violcode is not null                      
            	Group By cuisinecode, violcode
            	Having InspCount > 100
            ) As I
            Inner Join (
            	Select violcode, Count(*) As ViolCount
            	From  grades
            	Where violcode is not null
            	Group By violcode
            ) As V On I.violcode = V.violcode
            Left Join (
            	Select cuisinecode, Count(*) As CuiCount
            	From grades
            	Group by cuisinecode
            ) as C on I.CUISINECODE = C.CUISINECODE
            Cross Join (
            	Select Count(*) As TotalCount
            	From grades
            	Where cuisinecode is not null and violcode is not null   
            ) as T
            Inner Join (
            	Select violationcode, violationdesc
            	from violations
            	where date(enddate) > date('2014-01-01')
            ) as VDes on VDes.VIOLATIONCODE=I.VIOLCODE
            Left Join cuisines on cuisines.CuisineCode = I.CuisineCode
            Order by Ratio DESC
            Limit 20"""
    k= c.execute(sqlquery)
    return k.fetchall()  
    #return [(("Café/Coffee/Tea", "Toilet facility not maintained and provided with toilet paper; waste receptacle and self-closing door."), 1.8836420929815939, 315)] * 20



        
#My Code
import pystaggrelite3
import sqlite3
import sys

# Settings        
reload(sys)
sys.setdefaultencoding('utf-8')

# Set up SQLIte
con = sqlite3.connect('sqlproject.sqlite')

# Add aggregate function "stderr" from pystaggrelite3
con.create_aggregate("stderr", 1, pystaggrelite3.sem)


#To get the results, uncomment the following function
#score_by_zipcode()
#score_by_map()
#score_by_borough()
#score_by_cuisine()
#violation_by_cuisine()
