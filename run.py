import bs4
import json
import requests

emojis = []

with open('microsoft.html', 'r', encoding='utf-8') as f:
    soup = bs4.BeautifulSoup(f.read(), 'html.parser')

    # Find all the emoji names
    data = soup.select('.emoji-grid > li > a')

    for emoji in data:
        path = emoji['href']
        response = requests.get(f'https://emojipedia.org{path}')
        soup = bs4.BeautifulSoup(response.text, 'html.parser')

        # Find the emoji name
        emoji_char = soup.select_one('h1 > span').text
        emoji_name = soup.select_one('h1').text.strip()
        emoji_desc = soup.select_one('.description > p').text.strip()

        emojis.append({
            'emoji': emoji_char,
            'name': emoji_name,
            'description': emoji_desc
        })


# Write the list of emojis to a JSON file
with open('emojis.json', 'w', encoding='utf-8') as f:
    json.dump(emojis, f, indent=2, ensure_ascii=False)
