import scrapy


class SpiderArticle(scrapy.Spider):
    name = 'sa'
    allowed_domains = ['zen.yandex.ru']
    start_urls = ['https://zen.yandex.ru/media/kodkrasoty/kak-slojilas-sudba-dodo-chogovadze--aktrisy-kotoraia-v-14-let-sygrala-princessu-budur-v-filme-volshebnaia-lampa-aladdina-61276e12344fe2562d04203b']

    def parse(self, response, **kwargs):
        header = response.css('h1::text').get()
        print(header)
