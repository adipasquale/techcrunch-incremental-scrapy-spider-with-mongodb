# -*- coding: utf-8 -*-
import scrapy
import re
from tc_scraper.items import BlogPost
from dateutil import parser
from tc_scraper.mongo_provider import MongoProvider


class TechcrunchSpider(scrapy.Spider):
    name = 'techcrunch'
    allowed_domains = ['techcrunch.com']
    start_urls = ['http://techcrunch.com/']

    @classmethod
    def from_crawler(cls, crawler, **kwargs):
        settings = crawler.settings
        return cls(
            mongo_uri=settings.get('MONGO_URI'),
            mongo_database=settings.get('MONGO_DATABASE'),
            **kwargs
        )

    def __init__(self, limit_pages=None, mongo_uri=None, mongo_database=None, *args, **kwargs):
        super(TechcrunchSpider, self).__init__(*args, **kwargs)
        if limit_pages is not None:
            self.limit_pages = int(limit_pages)
        else:
            self.limit_pages = 0
        self.mongo_provider = MongoProvider(mongo_uri, mongo_database)
        self.collection = self.mongo_provider.get_collection()
        last_items = self.collection.find().sort("published_at", -1).limit(1)
        self.last_scraped_url = last_items[0]["url"] if last_items.count() else None

    def parse(self, response):
        for post in response.css(".post-block"):
            title = post.css(".post-block__title__link")
            url = title.css("::attr(href)").extract_first()
            if url == self.last_scraped_url:
                print("reached last item scraped, breaking loop")
                return
            yield scrapy.Request(url, callback=self.parse_post)
        if response.css(".load-more"):
            next_page_url = response.css(".load-more::attr(href)").extract_first()
            # urls look like https://techcrunch.com/page/4/
            match = re.match(r".*\/page\/(\d+)\/", next_page_url)
            next_page_number = int(match.groups()[0])
            if next_page_number <= self.limit_pages:
                yield scrapy.Request(next_page_url)

    def parse_post(self, response):
        item = BlogPost(
            title=response.css("h1::text").extract_first(),
            author=response.css(".article__byline>a::text").extract_first().strip(),
            published_at=self.extract_post_date(response),
            content=self.extract_content(response),
            url=response.url
        )
        yield(item)

    def extract_post_date(self, response):
        date_text = response.css("meta[name='sailthru.date']::attr(content)")
        return parser.parse(date_text.extract_first())

    def extract_content(self, response):
        paragraphs_texts = [
        p.css(" ::text").extract()
            for p in response.css(".article-content>p")
        ]
        paragraphs = ["".join(p) for p in paragraphs_texts]
        paragraphs = [re.subn("\n", "", p)[0] for p in paragraphs]
        paragraphs = [p for p in paragraphs if p.strip() != ""]
        return "\n\n".join(paragraphs)