# Web Scraping Homework - Mission to Mars

![mission_to_mars](Images/mission_to_mars.png)

In this assignment we visited NASA webpages for Mars News, Mars facts, Mars Featured image and Mars Hemispheres.

The requirement was to initially use Jupyter notebooks to create the code using BeautifulSoup, Pandas, and Requests/Splinter

Once the code was created, we used it to populate a python "scrape mars" document.

The methodology for each url "visit" was similar; define browser, define the URL, visit url, add relative pathway if needed. Once at the required site, I opened the console to identify the elements linked to the image/or text desired and used requests and beautiful soup to get and parse the html.

For the Mars Facts table, we needed to create a list for the column data, use pandas to read the data and then convert to html table structure.

For the hemispheres images, we needed to create a dictionary, adding each hemisphere image and title to a list.

All of these were then added to a mongo database, mars_db. 

Using mongo db and a flask application in app.py a scrape function was called, populating the database and data was then rendered to the webpage. 

Challenges: other than syntax and coding errors I had issues populating the webpage in a timely fashion. This resulted in the addition of a button feature that activated the scrape function (and which I left for the purpose of updating the page) but which did not consistently resolve the issue.

Finally, I understood the purpose of the .sleep() function, ( a eureka moment) which served to time the rendering of images to the execution of the index file. I added this function to each browser visit so the when the web page rendered it was fully executed.

Primary references for this homework included lessons through the program on (mongo) database creation, w3 schools (referenced within the code), help from tutor on the concept of creating a dictionary for the hemispheres, other references as documented.





Additional references:
#https://stackoverflow.com/questions/53604168/how-to-extract-a-part-of-url-from-dictionary-value-in-python

https://stackoverflow.com/questions/9198334/how-to-build-up-a-html-table-with-a-simple-for-loop-in-jinja2
