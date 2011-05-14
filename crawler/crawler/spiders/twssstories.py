from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from crawler.items import Twss

class TwssSpider(CrawlSpider):
    name = 'twssstories'
    allowed_domains = ['twssstories.com']
    start_urls = ['http://www.twssstories.com/']

    rules = (
        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(SgmlLinkExtractor(allow=('node\?page=[\d]+')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url)

        hxs = HtmlXPathSelector(response)
        for t in hxs.select("id('mainContent')/div[1]/div/p/text()"):
            t = t.extract()
            last = t.rfind('"')
            slast = t.rfind('"', 0, last-1)+1
            item = Twss()
            item["joke"] = t[slast:last]
            yield item
        #return item
