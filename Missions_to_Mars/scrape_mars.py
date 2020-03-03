from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

# This is for debugging

def savetofile(contents):
    file = open('_temporary.txt',"w",encoding="utf-8")
    file.write(contents)
    file.close()


def scrape():
    executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

# --------------------------------------------------------------------------------------------
    # NASA Mars News
    url_nasa = 'https://mars.nasa.gov/news/'

    browser.visit(url_nasa)
    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    # NASA MARS top news story - title
    news_title = soup.find('div', class_="content_title").text.strip()
    news_title

    # NASA MARS top news story - paragraph
    news_p = soup.find('div', class_="article_teaser_body").text.strip()
    news_p

# --------------------------------------------------------------------------------------------
    # JPL Mars Space Images
    url_jpl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_jpl)
    time.sleep(1)

    #click the button
    browser.find_by_id('full_image').first.click()
    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    marsimage = soup.find('img', class_="fancybox-image").get("src")
    baseurl = 'https://www.jpl.nasa.gov'
    featured_image_url = baseurl+marsimage
    featured_image_url

# --------------------------------------------------------------------------------------------
    # Mars Weather
url_weather = "https://twitter.com/marswxreport?lang=en"
browser.visit(url_weather)
time.sleep(3)

html = browser.html
soup = bs(html, "html.parser")

response = requests.get(url_weather)
time.sleep(1)

twitter_soup = bs(response.text, 'html.parser')
timeline = twitter_soup.select('#timeline li.stream-item')

all_tweets = []
for tweet in timeline:
    tweet_text = tweet.select('p.tweet-text')[0].get_text()
    all_tweets.append({"text": tweet_text})
mars_weather = all_tweets[0]
print(mars_weather)

# --------------------------------------------------------------------------------------------
    # Mars facts
    url = 'https://space-facts.com/mars/'
    browser.visit(url) # not necessary, but added for checking the operation
    time.sleep(1)

    dfs = pd.read_html(url)
    for df in dfs:
        try:
            df = df.rename(columns={0:"Description", 1:"Value"})
            df = df.set_index("Description")
            marsfacts_html = df.to_html().replace('\n', '')
            # df.to_html('marsfacts.html') # to save to a file to test
            break
        except:
            continue

# --------------------------------------------------------------------------------------------
    # Mars Hemispheres
    base_url = 'https://astrogeology.usgs.gov'
    url = base_url + '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    items = soup.find_all('div', class_='item')

    urls = []
    titles = []
    for item in items:
        urls.append(base_url + item.find('a')['href'])
        titles.append(item.find('h3').text.strip())

    img_urls = []
    for oneurl in urls:
        browser.visit(oneurl)
        time.sleep(1)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        oneurl = base_url+soup.find('img',class_='wide-image')['src']
        img_urls.append(oneurl)

    hemisphere_image_urls = []

    for i in range(len(titles)):
        hemisphere_image_urls.append({'title':titles[i],'img_url':img_urls[i]})

# --------------------------------------------------------------------------------------------
    # Assigning scraped data to a page
    marspage = {}
    marspage["news_title"] = news_title
    marspage["news_p"] = news_p
    marspage["featured_image_url"] = featured_image_url
    marspage["mars_weather"] = mars_weather
    marspage["marsfacts_html"] = marsfacts_html
    marspage["hemisphere_image_urls"] = hemisphere_image_urls

    return marspage