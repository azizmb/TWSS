from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from crawler.items import Twss

class TwssSpider(CrawlSpider):
    name = 'thatswhat-she-said'
    allowed_domains = ['thatswhat-she-said.com']
    start_urls = ['http://www.thatswhat-she-said.com/']

    rules = (
        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(SgmlLinkExtractor(allow=('/content/1/page/[\d]+')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url)

        hxs = HtmlXPathSelector(response)
        for t in hxs.select("/html/body/div/div[3]/div/div/div/div[2]/text()"):
            t = t.extract()
            item = Twss()
            t = t.replace('"', "")
            #print t
            item["joke"] = t
            yield item
        #return item
