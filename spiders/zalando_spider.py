import scrapy


class ZalandoSpiderSpider(scrapy.Spider):
    name = "zalando_spider"
    # start_urls = ["https://zalando.co.uk/mens-clothing"]

    def start_requests(self):
        for i in range(1,429):
            url = f'https://www.zalando.co.uk/mens-clothing/?p={i}'
            yield scrapy.Request(url=url, callback=self.parse_search_page)

    def parse_search_page(self, response):
        links = response.css("a._LM.tCiGa7.ZkIJC-.JT3_zV.CKDt_l.CKDt_l.LyRfpJ ::attr(href)").getall()
        for link in links:
            if "https" in link:
                yield scrapy.Request(url=link, callback=self.parse_item)

    def parse_item(self, response):
        title = response.css('.EKabf7.R_QwOV ::text').get()
        brand = response.css('.z2N-Fg.yOtBvf.FxZV-M.HlZ_Tf._5Yd-hZ ::text').get()
        price = response.css('.sDq_FX._4sa1cA.FxZV-M.HlZ_Tf ::text').get()
        # image_links = response.css('img.sDq_FX.lystZ1.FxZV-M._2Pvyxl.JT3_zV.EKabf7.mo6ZnF._1RurXL.mo6ZnF._7ZONEy ::attr(href)').getall()
        # main_image = image_links[0]
        yield {
            "Product Name": title,
            "Brand":brand,
            'Price':price,
            'Product Url': response.request.url
        }