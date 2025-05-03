import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from database.db import get_connection

def scrape_opportunities_for_youth():
    url = 'https://opportunitiesforyouth.org/category/scholarships/'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.select('article')

        conn = get_connection()
        cursor = conn.cursor()

        for card in cards:
            if card.h2:  # Check if h2 tag exists
                title = card.h2.text.strip()
                link_tag = card.find('a')
                link = link_tag['href'] if link_tag else None

                if not link:
                    continue  # Skip if no link

                provider = "Opportunities for Youth"
                eligibility = "Check official page"
                deadline = datetime.now().date()  # Placeholder (no real deadline available)

                # Check for duplicates
                cursor.execute("SELECT * FROM scholarships WHERE link = %s", (link,))
                if cursor.fetchone():
                    continue  # Already exists

                # Insert into database
                cursor.execute("""
                    INSERT INTO scholarships (name, provider, eligibility, deadline, link)
                    VALUES (%s, %s, %s, %s, %s)
                """, (title, provider, eligibility, deadline, link))
                conn.commit()

        cursor.close()
        conn.close()
        print("✅ Scraping completed successfully.")

    else:
        print(f"❌ Failed to retrieve data. Status code: {response.status_code}")

def scrape_scholarship_positions():
    url = 'https://scholarship-positions.com/'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        posts = soup.select('h2.entry-title')

        conn = get_connection()
        cursor = conn.cursor()

        for post in posts:
            title_tag = post.find('a')
            if title_tag:
                title = title_tag.text.strip()
                link = title_tag['href']

                if not link:
                    continue  # Skip if no link

                provider = "Scholarship Positions"
                eligibility = "Check official page"
                deadline = datetime.now().date()

                # Check for duplicates
                cursor.execute("SELECT * FROM scholarships WHERE link = %s", (link,))
                if cursor.fetchone():
                    continue

                # Insert into database
                cursor.execute("""
                    INSERT INTO scholarships (name, provider, eligibility, deadline, link)
                    VALUES (%s, %s, %s, %s, %s)
                """, (title, provider, eligibility, deadline, link))
                conn.commit()

        cursor.close()
        conn.close()
        print("✅ Scholarship Positions scraping completed successfully.")

    else:
        print(f"❌ Failed to scrape Scholarship Positions. Status code: {response.status_code}")



# Run the scraper
if __name__ == '__main__':
    scrape_opportunities_for_youth()
    scrape_scholarship_positions()

