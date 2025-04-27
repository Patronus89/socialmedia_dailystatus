# scraper.py
# Your scraping logic here
# scraper.py
# scraper.py
import newspaper
from newspaper import Article

def scrape_news(sources, max_articles_per_source=5):
    articles = []
    for site_url in sources:
        try:
            paper = newspaper.build(site_url, memoize_articles=False)
            count = 0
            for content in paper.articles:
                if count >= max_articles_per_source:
                    break
                content.download()
                content.parse()
                articles.append(content.text)
                count += 1
        except Exception as e:
            print(f"Error scraping {site_url}: {e}")
    return articles

def collect_data(keywords=None):
    news_sources = [
        "https://www.mmtimes.com/",
        "https://www.irrawaddy.com/",
        "https://www.frontiermyanmar.net/en",
        "https://www.bbc.com/burmese",
        "https://www.channelnewsasia.com/asia",
        "https://www.nhk.or.jp/nhkworld/en/news/",
    ]
    news_articles = scrape_news(news_sources)
    return news_articles


print("Scraping news and Twitter...")