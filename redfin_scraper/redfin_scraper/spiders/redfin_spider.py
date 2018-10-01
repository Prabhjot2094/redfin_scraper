import time
import scrapy
from redfin_scraper.items import HouseItem
from redfin_scraper.items import AddressItem
from redfin_scraper import config

class Redfin(scrapy.Spider):

    name = "redfin"

    start_urls = ["https://www.redfin.com"]

    max_price = 10
    min_price = 0
    
    def parse(self, response):
        #Iterate over all cities on the homepage
        filters = "/filter/include=sold-all,min-price={}k,max-price={}k".format(self.min_price, self.max_price)
        for city in response.xpath("//*[@id=\"content\"]/div[3]/div[6]/section/div/ul/li"):
            url = "https://www.redfin.com"+city.xpath("a/@href").extract()[0]+filters
            return scrapy.Request(url, callback = self.modify_download_filters)

    def process_sold_homes(self, response):
        print(response.url)
        #Itemize data received on modifying the download_all link
        raw_data = response.text.strip()
        rows = raw_data.split("\n")
        
        #headers = ['SALE TYPE', 'SOLD DATE', 'PROPERTY TYPE', 'ADDRESS', 'CITY', 'STATE', 'ZIP', 'PRICE', 'BEDS', 'BATHS', 'LOCATION', 'SQUARE FEET', 
        #        'LOT SIZE', 'YEAR BUILT', 'DAYS ON MARKET', 'SQUARE FEET', 'HOA MONTH', 'STATUS', 'NEXT OPEN HOUSE START TIME', 'NEXT OPEN HOUSE END TIME', 
        #        'URL', 'SOURCE', 'MLS', 'FAVORITE', 'INTERESTED', 'LATITUDE', 'LONGITUDE'] 
        
        #for i in range(len(config.HEADERS)):
        #    headers[i] = headers[i].replace(" ","_")
        
        #each row corresponds to a particular house
        for row in rows[1:-1]:
            house = HouseItem()
            address = AddressItem()
            for header, val in zip(config.HEADERS, row.split(",")):
                if header in config.ADDRESS_FIELDS:
                    address[header] = val.strip()
                elif header in config.HOUSE_FIELDS:
                    house[header] = val.strip()
                else:
                    continue

            yield house

    def modify_download_filters(self, response):
        #Modify search filter till the result count<10000 as redfin returns atmost 10k results
        #Once the result count is less than 10k, scrape all of them and increase the filter values
        #Filtering currently done on price. Works fine but can be done using a combo of other filters as well
        search_stats = response.xpath("//*[@id=\"sidepane-header\"]/div[2]/div/div[1]/text()").extract()

        #CASE NOT HANDLED : If no houses bw current search params, they can be beyond the search
        #The above case is avoided by taking a large starting price
        if not search_stats:
            yield None

        else:
            no_of_homes = max([int(item) if item.isdigit() else 0 for item in search_stats[0].split()])

            request_url = response.url.split("filter")[0]
            print("Number of homes = {}, url = {}, meta={}".format(no_of_homes, response.url, response.meta.get("root")))
            if no_of_homes>10000:
                if self.min_price!=0:
                    filter_value = "filter/max-price={}k,min-price={}k,include=sold-all" 
                else:
                    filter_value = "filter/max-price={}k,include=sold-all" 
            
                self.max_price = self.max_price/2
                request_url += filter_value.format(self.max_price, self.min_price)
                yield scrapy.Request(request_url, callback = self.modify_download_filters)
                #no_of_homes = max([int(item) if item.isdigit() else 0 for item in search_stats.split()])
            else:
                print("---------------------------------")
                download_url = response.xpath("//*[@id=\"download-and-save\"]/@href").extract()[0]
                download_url = download_url.replace("num_homes=350","num_homes=100000")
                
                #Allows for rapid increment is low number of houses found in current range
                max_filter_increment = (10000/no_of_homes)*(self.max_price-self.min_price)
                
                self.min_price = self.max_price+1
                self.max_price += max_filter_increment
                #if self.min_price!=0:
                filter_value = "filter/max-price={}k,min-price={}k,include=sold-all" 
                #else:
                #    filter_value = "filter/max-price={}k,include=sold-all" 
            
                #download_url +=("&max_price={}".format(self.max_price))

                #if self.min_price!=0:
                #    download_url+=("&min_price={}".format(self.min_price))

                download_url = self.start_urls[0]+download_url
                print(download_url)
                #for i in range(3):
                print("\a")
                #    time.sleep(1)
                #print("*"*15,download_url)

                next_filter_url = request_url+filter_value.format(self.max_price, self.min_price)
                yield scrapy.Request(next_filter_url, callback = self.modify_download_filters)

                yield scrapy.Request(download_url, callback = self.process_sold_homes)

