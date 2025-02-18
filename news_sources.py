from textmine.webscrape import *

def select_scraper(news_scrapers_, domain):
    scraper_domains = news_scrapers_.keys()
    for key in scraper_domains:
        if key in domain:
            return key
    return None

news_scrapers = {
    ScrapeAPContent.get_domain(): ScrapeAPContent(),
    ScrapeCNNContent.get_domain(): ScrapeCNNContent(),
    ScrapeNYTContent.get_domain(): ScrapeNYTContent(),
    ScrapeBBCContent.get_domain(): ScrapeBBCContent(),
    ScrapeMSNBCContent.get_domain(): ScrapeMSNBCContent(),
    ScrapeNewYorkPostContent.get_domain(): ScrapeNewYorkPostContent(),
    ScrapeMotherJonesContent.get_domain(): ScrapeMotherJonesContent(),
    ScrapeCenterSquareContent.get_domain(): ScrapeCenterSquareContent(),
    ScrapeDispatchContent.get_domain(): ScrapeDispatchContent(),
    ScrapeOANNContent.get_domain(): ScrapeOANNContent(),
    ScrapeABCContent.get_domain(): ScrapeABCContent()
}

print()