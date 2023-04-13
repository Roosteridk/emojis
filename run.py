import bs4
import json
import requests
import time

emojis = []

with open('microsoft.html', 'r', encoding='utf-8') as f:
    soup = bs4.BeautifulSoup(f.read(), 'html.parser')

    # Find all the emoji names
    data = soup.select('.emoji-grid > li > a')

    for emoji in data:
        path = emoji['href']

        while True:
            try:
                response = requests.get(f'https://emojipedia.org{path}', headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
                }, timeout=10)
                response.raise_for_status()
            except:  # noqa: E722
                time.sleep(5)
                continue
            break

        soup = bs4.BeautifulSoup(response.text, 'html.parser')

        # Find the emoji name
        emoji_char = soup.select_one('#emoji-copy').attrs['value']
        emoji_name = emoji.select_one('img').attrs['alt']
        emoji_desc = soup.select_one('.description > p').text.strip()

        emojis.append({
            'emoji': emoji_char,
            'name': emoji_name,
            'description': emoji_desc
        })

        print(f'{emoji_name} {emoji_char}')


# Write the list of emojis to a JSON file
with open('emojis.json', 'w', encoding='utf-8') as f:
    json.dump(emojis, f, indent=2, ensure_ascii=False)
