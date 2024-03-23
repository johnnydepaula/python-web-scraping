import pandas as pd
import requests
from bs4 import BeautifulSoup

pages = 2 # The ammount of pages to scrap
categories = ['news', 'sports', 'politics', 'business'] # The category of the page to scrap
articles = []

for category in categories:
    url = f'https://punchng.com/topics/{category}'

    # < When getting Access Denied, try the workaround bellow,
    # thanks to Anderson from StackOverflow for the tip >
    # headers = {'User-Agent': 'Mozilla/5.0'}
    # response = requests.get(url, headers=headers).text

    response = requests.get(url).text


    soup = BeautifulSoup(response, 'html.parser')

    article_container = soup.find('div', class_='latest-news-timeline-section')


    article_temp = article_container.find_all_next('article')



    for article in article_temp:
        title = article.find('h1', class_='post-title').text.strip()
        excerpt = article.find('p', class_='post-excerpt').text.strip()
        date = article.find('span', class_='post-date').text.strip()
        link = article.find('a')['href']

        articles.append({
            'category': category,
            'title': title,
            'excerpt': excerpt,
            'date': date,
            'link': link
        })

    for article in articles:
        article_page = requests.get(article['link']).text

        article_soup = BeautifulSoup(article_page, 'html.parser')
        article['author'] = article_soup.find('span', class_='post-author').text.replace('By ', '').strip()
        article['content'] = article_soup.find('div', class_='post-content').text.replace('By ', '').strip()

        if article_soup.find('div', class_='post-image-wrapper') is None:
            article['image'] = ''
        else:
            article['image'] = article_soup.find('div', class_='post-image-wrapper').find_next('figure').find_next('img')['src']

    print(f'Data successfully scraped.')

articles_df = pd.DataFrame(articles)
articles_df.to_csv('articles-data.csv', index=False)

print('Scraping Job complete.')
