import scrapy
import csv
from PIL import Image
import os


class HotlineSpider(scrapy.Spider):
    name = "hotline"
    allowed_domains = ["hotline.com"]
    start_urls = ["http://hotline.com/"]

    def parse(self, response):
        laptops = response.css("div.item-info")

        for laptop in laptops:
            name = laptop.css("a.item-name::text").get().strip()

            price = laptop.css("div.item-price::text").get().strip()

            url = laptop.css("a.item-name::attr(href)").get()

            store_name = laptop.css("div.item-shop::text").get().strip()

            store_logo_url = laptop.css("div.item-shop img::attr(src)").get()

            data = {
                "name": name,
                "price": price,
                "url": url,
                "store_name": store_name,
                "store_logo_url": store_logo_url,
            }

            image_url = laptop.css("img::attr(data-original)").get()
            yield scrapy.Request(
                url=image_url,
                meta={"data": data},
                callback=self.save_image_and_thumbnail,
                priority=1,
            )

        with open('laptops.csv', mode='w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['brand', 'model', 'price', 'image_url', 'image_local_path']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()

            for laptop in laptops:
                image_url = laptop['image_url']
                image_name = image_url.split('/')[-1]
                image_path = f'images/{image_name}'

                if not os.path.exists(image_path):
                    with open(image_path, 'wb') as img_file:
                        img_file.write(scrapy.get(image_url).content)

                with Image.open(image_path) as img:
                    img.thumbnail((50, 50))
                    thumbnail_path = f'images/thumbnails/{image_name}'
                    img.save(thumbnail_path)

                laptop['image_local_path'] = thumbnail_path
                writer.writerow(laptop)