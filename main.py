from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Import your spider class
from wikicrawl.spiders.wiki import WikiSpider


def run_spider():
    # Initialize the Scrapy settings
    settings = get_project_settings()

    # Instantiate the CrawlerProcess with settings
    process = CrawlerProcess(settings=settings)

    # Add your spider to the process
    process.crawl(WikiSpider)

    # Start the crawling process
    process.start()


if __name__ == "__main__":
    run_spider()
