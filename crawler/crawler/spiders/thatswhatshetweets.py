from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from crawler.items import Twss

class TwssSpider(CrawlSpider):
    name = 'thatswhatshetweets'
    allowed_domains = ['thatswhatshetweets.com']
    start_urls = ['http://www.thatswhatshetweets.com']
    rules = (
        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(SgmlLinkExtractor(allow=('page/[\d]+/')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url)

        hxs = HtmlXPathSelector(response)
        for t in hxs.select("id('pagecontent')/div/div/p/a/text()"):
            t = t.extract()
            item = Twss()
            t = t.replace('"', "")
            t = t.strip()
            #print t
            item["joke"] = t
            yield item
        #return item
