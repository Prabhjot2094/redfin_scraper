Following are the dependencies:
	-Tor : Allows us to redfin from various ip addresses. One gets blocked get a new one Port 9050
	-Polipo : Proxy server for scrapy and tor as scrapy does not work with SOCKS port 8123
	-Scrapy
	
To write data to the DB:
	-Set the db details in the config.py file
	-Modify the sql query in the class RedfinScraperDBPipeline(pipeline.py)

To write to a file #Not recommended:
	-In settings.py uncomment RedfinScraperPipeline

To run the project : scrapy crawl redfin (Inside redfin)

To write the data of one city in the csv:
	-Replace yield with return in spider/redfin_spider.py
