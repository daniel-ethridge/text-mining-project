import csv

RAW_ARTICLES = "../text-mining-project-data/dirty/raw-article-data.csv"

def create_count_vectorized_dataframe(max_features, ):
with open(RAW_ARTICLES) as f:
    reader = csv.reader(f, delimiter=",")
    for row in reader:
        raw_articles.append(row)

