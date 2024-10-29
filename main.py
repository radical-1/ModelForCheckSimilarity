from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import random
import string

# List of predefined users
users = ['elonmusk', 'JeffBezos', 'Cristiano']  # some random users


def generate_random_tweet_url(user):
    base_url = 'https://x.com/'
    tweet_id = ''.join(random.choices(string.digits, k=18))  # Generate an 18-digit random number
    return f"{base_url}{user}/status/{tweet_id}"


def check_tweet_url_validity(url):
    # Set up Selenium with Chrome WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    service = Service('/usr/bin/chromedriver')  # Replace with the path to your chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open the URL
    driver.get(url)

    # Wait for the page to load
    time.sleep(5)  # Adjust the sleep time as needed

    # Get the page source
    page_source = driver.page_source

    # Close the browser
    driver.quit()

    # Parse the HTML content
    soup = BeautifulSoup(page_source, 'html.parser')

    # Check for tweet content
    tweet_content = soup.find('div', {'data-testid': 'tweetText'})
    return tweet_content is not None

# Generate a list of random tweet URLs for predefined users and check their validity
valid_tweet_urls = []
for user in users:
    for _ in range(10):  # Generate 10 random tweets per user
        url = generate_random_tweet_url(user)
        if check_tweet_url_validity(url):
            valid_tweet_urls.append(url)

# Print the valid URLs
for url in valid_tweet_urls:
    print(url)
