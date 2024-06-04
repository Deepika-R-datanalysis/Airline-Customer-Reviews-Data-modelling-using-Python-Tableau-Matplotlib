pip install requests
pip install beautifulsoup4


import requests
from bs4 import BeautifulSoup
import csv

def scrape_reviews(url):
    # Fetch the web page
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
    else:
        print(f"Failed to retrieve the web page. Status code: {response.status_code}")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the reviews
    reviews = soup.find_all('div', class_='body')  # Adjust the tag and class as per actual HTML structure

    review_data = []
    for review in reviews:
        review_text = review.find('h2', class_='text_header').text.strip()  # Adjust tag and class
        reviewer_name = review.find('span', itemprop='name').text.strip()  # Adjust tag and class
        reviewed_date = review.find('time', itemprop='datePublished').text.strip()
        review_body = review.find('div', class_='text_content', itemprop='reviewBody').text.strip()
        review_data.append([reviewer_name, review_text, reviewed_date,review_body])

    return review_data


def save_reviews_to_csv(review_data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Reviewer', 'Review'])  # Write header
        writer.writerows(review_data)  # Write data


url = 'https://www.airlinequality.com/airline-reviews/british-airways'
reviews = scrape_reviews(url)

if reviews:
    csv_file = 'reviews.csv'
    save_reviews_to_csv(reviews, csv_file)
    print(f"Reviews have been saved to {csv_file}")
else:
    print("No reviews found or failed to scrape the reviews.")
