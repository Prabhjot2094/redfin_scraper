import time
import scrapy
from redfin_scraper.items import HouseItem

class Redfin(scrapy.Spider):

    name = "redfin"

    start_urls = ["https://www.redfin.com"]

    max_price = 10
    min_price = 0
    #def start_request():
    #    return scrapy.Request(start_urls[0],headers={'User-Agent': 'My User Agent 1.0', 'From': 'youremail@domain.com'})
    
    def parse(self, response):

        filters = "/filter/include=sold-all,min-price={}k,max-price={}k".format(self.min_price, self.max_price)
        for city in response.xpath("//*[@id=\"content\"]/div[3]/div[6]/section/div/ul/li"):
            url = "https://www.redfin.com"+city.xpath("a/@href").extract()[0]+filters
            return scrapy.Request(url, callback = self.get_optimum_filters, meta={"root":1})

    def download_sold_homes(self, response):
        print(response.url)
        search_stats = response.xpath("//*[@id=\"sidepane-header\"]/div[2]/div/div[1]/text()").extract()[0]

        no_of_homes = max([int(item) if item.isdigit() else 0 for item in search_stats.split()])

        #print("Number of homes = {}".format(no_of_homes))
        #if no_of_homes>10000:
            #Get the filter resultig in <10K results as redfin returns atmost 10k results
        filter_url = response.url+",min-price={}k,max-price={}k,include=sold-all".format(self.min_price, self.max_price)
        print("*"*15,filter_url)
        return scrapy.Request(filter_url, callback = self.get_optimum_filters)
        
        """
        download_url = response.xpath("//*[@id=\"download-and-save\"]/@href").extract()[0]
        download_url = download_url.replace("num_homes=350","num_homes=100000")
        download_url +=("&max_price={}".format(self.max_price))

        if self.min_price!=0:
            download_url+=("&min_price={}".format(self.min_price))

        download_url = self.start_urls[0]+download_url
        print(download_url)
        for i in range(3):
            print("\a")
            time.sleep(1)
        print("*"*15,download_url)
        return scrapy.Request(download_url, callback = self.process_sold_homes)
        """

    def process_sold_homes(self, response):
        print(response.url)
        raw_data = response.text.strip()
        rows = raw_data.split("\n")
        
        headers = ['SALE TYPE', 'SOLD DATE', 'PROPERTY TYPE', 'ADDRESS', 'CITY', 'STATE', 'ZIP', 'PRICE', 'BEDS', 'BATHS', 'LOCATION', 'SQUARE FEET', 
                'LOT SIZE', 'YEAR BUILT', 'DAYS ON MARKET', 'SQUARE FEET', 'HOA MONTH', 'STATUS', 'NEXT OPEN HOUSE START TIME', 'NEXT OPEN HOUSE END TIME', 
                'URL', 'SOURCE', 'MLS', 'FAVORITE', 'INTERESTED', 'LATITUDE', 'LONGITUDE'] 
        
        for i in range(len(headers)):
            headers[i] = headers[i].replace(" ","_")
        
        #print(headers)
        for row in rows[:-1]:
            house = HouseItem()
            for header, val in zip(headers, row.split(",")):
                house[header] = val.strip()

            yield house

    def get_optimum_filters(self, response):
        search_stats = response.xpath("//*[@id=\"sidepane-header\"]/div[2]/div/div[1]/text()").extract()[0]

        if not search_stats:
            print("EXITINGGGGGGGGG, Search Stats = {}".format(search_stats))
            yield None
        else:
                #self.min_price = self.max_price+1
                #self.max_price += 100000 

            no_of_homes = max([int(item) if item.isdigit() else 0 for item in search_stats.split()])

            request_url = response.url.split("filter")[0]
            print("Number of homes = {}, url = {}, meta={}".format(no_of_homes, response.url, response.meta.get("root")))
            if no_of_homes>10000:
                if self.min_price!=0:
                    filter_value = "filter/max-price={}k,min-price={}k,include=sold-all" 
                else:
                    filter_value = "filter/max-price={}k,include=sold-all" 
            
                self.max_price = self.max_price/2
                request_url += filter_value.format(self.max_price, self.min_price)
                yield scrapy.Request(request_url, callback = self.get_optimum_filters)
                #no_of_homes = max([int(item) if item.isdigit() else 0 for item in search_stats.split()])
            else:
                print("---------------------------------")
                download_url = response.xpath("//*[@id=\"download-and-save\"]/@href").extract()[0]
                download_url = download_url.replace("num_homes=350","num_homes=100000")

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
                yield scrapy.Request(next_filter_url, callback = self.get_optimum_filters)

                yield scrapy.Request(download_url, callback = self.process_sold_homes)

