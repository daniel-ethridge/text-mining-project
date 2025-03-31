import textmine.api as tm_api
import textmine.webscrape as tm_web
import textmine.parse_json as tm_parse


def test_for_string(desired_strings: list, string_to_test):
    """
    Tests to see if any desired strings are in the test string
    :param desired_strings: A list of strings to iteratively test to see if they are in string_to_test
    :param string_to_test: A string to test for whether or not any of the desired strings are included
    :return: True if string_to_test has any of the desired strings. False otherwise
    """
    for desired_string in desired_strings:
        if desired_string in string_to_test:
            return True

    return False


def create_domain_multilist(domains: list) -> list:
    """
    Convert a list of domains into a proper list of domains for newsapi.org
    :param domains: list of domains
    :return: A list of strings. Each string is up to 20 domains comma separated
    """
    i = 0
    domain_list = []
    while True:
        if len(domains) <= 20 + i:
            domain_list.append(",".join(domains[i:len(domains)]))
            return domain_list
        else:
            domain_list.append(",".join(domains[i:i+20]))
            i += 20


if __name__ == "__main__":
    # Configuration
    ARTICLE_URLS = "../text-mining-project-data/dirty/article-urls.csv"
    GET_NYT_URLS = True
    GET_NEWS_API_URLS = True
    GET_NYPOST_URLS = False
    GET_AP_URLS = False
    GET_MOTHER_JONES_URLS = False
    GET_OANN_URLS = False

    if GET_NYT_URLS:
        nyt_api = tm_api.read_api_key_from_file("../api_keys/nyt-api-key.txt")

        # Handle NYT
        article_urls = []
        nyt_news = tm_api.NytApi(nyt_api)
        for page in range(0, 101):
            success, data = nyt_news.q("mass shootings").page(page).get()
            print(data)

            if not success:
                break

            # parse nyt_data
            for doc in data["response"]["docs"]:
                article_urls.append(doc["web_url"])

        with open(ARTICLE_URLS, "w") as f:
            f.write(",".join(article_urls))

    if GET_NEWS_API_URLS:
        with open(ARTICLE_URLS, "r") as f:
            article_urls = f.read().split(",")

        # Get API key for newsapi.org
        news_api = tm_api.read_api_key_from_file("../api_keys/news-api-key.txt")
        everything_news = tm_api.NewsApiDotOrgEverything(news_api, tm_parse.ParseNewsApiDotOrg())

        for page in range(1, 101):
            success, data = everything_news.q("mass shootings").page(page).get()
            print(data)

            if not success:
                break

            # parse nyt_data
            for doc in data:
                article_urls.append(doc["url"])

        with open("../text-mining-project-data/article-urls.csv", "w") as f:
            f.write(",".join(article_urls))

    if GET_NYPOST_URLS:
        with open(ARTICLE_URLS, "r") as f:
            article_urls = f.read().split(",")

        nypost = tm_web.ScrapeNewYorkPostContent()
        links = nypost.get_search_results("mass shooting", 1000)

        for link in links:
            article_urls.append(link)

        with open(ARTICLE_URLS, "w") as f:
            f.write(",".join(article_urls))

    if GET_AP_URLS:
        with open(ARTICLE_URLS, "r") as f:
            article_urls = f.read().split(",")

        ap = tm_web.ScrapeAPContent()

        print("getting ap links")
        links = ap.get_search_results("mass shooting", 1000)
        print("finished getting ap links")

        for link in links:
            article_urls.append(link)

        with open(ARTICLE_URLS, "w") as f:
            f.write(",".join(article_urls))

    if GET_OANN_URLS:
        with open("../text-mining-project-data/article-urls.csv", "r") as f:
            article_urls = f.read().split(",")

        oann = tm_web.ScrapeOANNContent()

        print("getting oann links")
        links = oann.get_search_results("mass shooting", 1000)
        print("finished oann getting links")

        for link in links:
            article_urls.append(link)

        with open("../text-mining-project-data/article-urls.csv", "w") as f:
            f.write(",".join(article_urls))

    if GET_MOTHER_JONES_URLS:
        with open(ARTICLE_URLS, "r") as f:
            article_urls = f.read().split(",")

        mother = tm_web.ScrapeMotherJonesContent()

        print("getting mother links")
        links = mother.get_search_results("mass shooting", 1000)
        print("finished mother getting links")

        for link in links:
            article_urls.append(link)

        with open(ARTICLE_URLS, "w") as f:
            f.write(",".join(article_urls))

    with open(ARTICLE_URLS, "r") as f:
        article_urls = f.read().split(",")
