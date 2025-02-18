from newspaper import Article
from newspaper.article import ArticleException
from urllib.parse import urlparse
import csv


def report_progress(num_processed_, num_failed_, total):
    if num_processed_ % 20 != 0:
        return

    print("+++++++++++++++++")
    print(f"Status: {100*num_processed_/total}%")
    print(f"Percent failed: {100*num_failed_/total}%")
    print("+++++++++++++++++")


with open("../text-mining-project-data/dirty/article-urls.csv", "r") as f:
    article_urls = f.read().split(",")

article_titles = []
article_text = []
article_domains = []
num_urls_processed = 0
num_failed = 0

for url in article_urls:
    try:
        article = Article(url)
        article.download()
        article.parse()

    except ArticleException:
        num_urls_processed += 1
        num_failed += 1
        report_progress(num_urls_processed, num_failed, len(article_urls))
        continue

    article_titles.append(article.title)
    article_text.append(article.text)
    article_domains.append(url)

    num_urls_processed += 1
    report_progress(num_urls_processed, num_failed, len(article_urls))

article_titles = [title.replace(",", "") for title in article_titles]
article_text = [
    text
    .replace(",", "")
    .replace("\"", "")
    .replace("”", "")
    .replace("“", "")
    .replace("’", "")
    .replace("(", "")
    .replace(")", "")
    .replace("-", " ")
    .replace("a.m.", "")
    .replace("p.m.", "")
    .replace(".", "")
    .replace("?", "")
    .replace("!", "")
    .replace(":", "")
    .replace(";", "")
    .replace("\n", " ")
    .lower()
    for text in article_text
]
article_domains = [domain.replace(",", "") for domain in article_domains]

full_article_data = [[domain, title, text] for domain, title, text in zip(article_domains, article_titles, article_text)]
with open("../text-mining-project-data/dirty/raw-article-data.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(full_article_data)