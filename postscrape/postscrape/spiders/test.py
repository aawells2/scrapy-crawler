import scrapy

class PostsSpider(scrapy.Spider):
    name = "card"
    
    custom_settings = {
        'DEPTH_LIMIT': 1,
        'DEPTH_PRIORITY': 1,
    }
    

    def start_requests(self):
        urls = [
            "https://lawforkids.org",
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        if 'text/html' in response.headers.get('Content-Type').decode(): # Skipping non-HTML content
            for card in response.css("div.card-body"):
                title = card.css("h5.card-title::text").get(default="").strip()
                if title == "Nominate an LRE Officer of the Year":
                    yield {
                           "Url": response.url,
                    }
        
            # Get all the links on the current page
            for a_tag in response.css('a'):
                link = a_tag.css('::attr(href)').get()
                if link: # If a link was found
                    absolute_link = response.urljoin(link)
                    # Check if it is an external link
                    if ("https://lawforkids.org" in absolute_link):
                        yield scrapy.Request(url=absolute_link, callback=self.parse)
