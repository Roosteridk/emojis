import requests
import csv
import re
import bs4
import json


def unicode_slugify(text):
    """
    Convert Unicode text into a slug.
    """
    # Replace non-ASCII characters with their closest ASCII equivalent
    text = ''.join((c if ord(c) < 128 else ' ' for c in text))
    # Convert whitespace and punctuation to dashes
    text = re.sub(r'[-\s]+', '-', text)
    # Remove any remaining non-word characters
    text = re.sub(r'[^\w-]+', '', text)
    # Convert to lowercase and return
    return text.lower()


def emoji_slugify(emoji_name):
    """
    Convert an emoji name into a slug.
    """
    # Remove any leading/trailing whitespace and lowercase the string
    emoji_name = emoji_name.strip().lower()
    # Replace all non-word characters with spaces
    emoji_name = re.sub(r'[^\w\s]+', ' ', emoji_name)
    # Replace spaces with dashes and return the result
    return unicode_slugify(emoji_name.replace(' ', '-'))


# Convert the CSV file to a list of dictionaries
# https://www.kaggle.com/datasets/eliasdabbas/emoji-data-descriptions-codepoints
with open('emoji_df.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    data = list(reader)


emojis = []

# Loop through the list of emojis
for row in data:
    emoji_name = row['name']
    # Skip duplicate emoji names
    if emoji_name == emojis[-1]['name']:
        continue

    emoji_slug = emoji_slugify(emoji_name)

    # Scrape emojipedia page
    url = f'https://emojipedia.org/{emoji_slug}/'
    response = requests.get(url)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    # Find the emoji image
    emojis.append({
        'name': emoji_name,
        'description': soup.select_one('.description > p').text,
    })

# Write the list of emojis to a JSON file
with open('emojis.json', 'w', encoding='utf-8') as f:
    json.dump(emojis, f, indent=2, ensure_ascii=False)
