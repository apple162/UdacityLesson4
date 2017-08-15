#!/usr/bin/python3
'''Imports the module for Postgre SQL'''
import psycopg2

'''Connect to the database'''
pg = psycopg2.connect("dbname = news")

'''Create cursor to interact with the database'''
c = pg.cursor()  

'''Create view of Author, Article Title, and a Log of Path that match Article Titles'''
c.execute("CREATE VIEW urls AS "\
          "SELECT articles.author, articles.title, log.path "\
          "FROM articles, log "\
          "WHERE log.path LIKE CONCAT('/article/', articles.slug,'%')")

'''Select the Title and Occurences of the most popular articles in the log'''
c.execute("SELECT title, count(*) AS num "\
          "FROM urls "\
          "GROUP BY title ORDER BY num desc LIMIT 3")

'''Fetch results'''
results1 = (c.fetchall())

'''Print results in a formatted manner'''
print("Most Popular Articles:")  
for i in results1:
    print(' "' + i[0] + ' "' + ' - ' + str(i[1]) + ' views')
print()

'''Select the Author Name and Total View times of their articles '''
c.execute("SELECT authors.name, count(*) AS num "\
          "FROM urls JOIN authors ON authors.ID = urls.author "\
          "GROUP BY authors.name Order By num desc")

'''Fetch results'''
results2 = (c.fetchall())

'''Print results'''
print("Most Popular Authors:")  
for x in results2:
    print(x[0] + ' - ' + str(x[1]) + ' views')
print()

'''Create view for dates where log status was error 4--'''
c.execute("create view errors as select CAST(time AS date) from log where status LIKE '4%%'")

'''Create view that shows the date and number of errors on that day'''
c.execute("create view errors2 as select time , count(*) as num from errors GROUP BY time Order by num desc")  

'''Create view that shows dates of logs actions'''
c.execute("create view total as select CAST(time AS date) from log")

'''Create view of total logs in each day'''
c.execute("create view total2 as select time, count(*) as num from total Group By time Order by num desc")  

'''Calculate and display the days where the errors made up over 1.5% of all logs'''
c.execute("SELECT errors2.time, 100*(CAST(errors2.num as float)/CAST(total2.num as float)) "\
          "FROM errors2 JOIN total2 ON errors2.time = total2.time "\
          "WHERE 100*(CAST(errors2.num as float)/CAST(total2.num as float)) > 1.5")

'''Fetch results'''
result3 = (c.fetchall())

'''Print Formatting'''
print("Days with >1.5% errors: ")
format = "%a %b %d %Y"  
right = result3[0][0]
s = right.strftime(format)
print(s + ' - ' + str(round(result3[0][1], 2)) + '% errors')

'''Close connection to DB'''
pg.close()

