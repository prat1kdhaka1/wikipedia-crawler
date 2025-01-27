﻿# wikipedia-crawler
Clone the repository

Install requirements: **pip install -r requirements.txt**

To run the crawler: **python main.py**

To add categories, open the **config.py** and add the name of the cateogry
<br>and the number of search results that category has.


<br>To find the number of search results a category has:

<br>Open this link: **https://ne.wikipedia.org/w/api.php?action=query&list=search&srsearch={NAME_OF_THE_CATEGORY}&srlimit=500&sroffset=0&format=json**


The number of search results is inside : **query["searchinfo"]["totalhits"]**
