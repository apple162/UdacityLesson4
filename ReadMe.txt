# Create view containing article titles and authors that have shown up in the log  
c.execute("create view urls as select articles.title from articles, log where articles.slug = trim(leading log.path, '/article/')")  

 # Create view of errors on given dates:  
c.execute("create view errors as select CAST(time AS date) from log where status LIKE '4%%'")  

# Create view of counts of errors on each date:
c.execute("create view errors2 as select time , count(*) as num from errors GROUP BY time Order by num desc")    

# Create view of dates in log
c.execute("create view total as select CAST(time AS date) from log")   

# Create count of logs on each date
c.execute("create view total2 as select time, count(*) as num from total Group By time Order by num desc")   

To execute the code, ensure that you are in vagrant virtual machine, and that you are in the same path as the python file.

Simply type “python3 logsanalysis.py” to run the program and retrieve the results.
