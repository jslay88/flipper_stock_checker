import json
import os

import requests
from bs4 import BeautifulSoup


WEBHOOK_URL = os.getenv('WEBHOOK_URL')
if not WEBHOOK_URL:
    raise ValueError('No WEBHOOK_URL provided')


def send_notification(message: str):
    requests.post(
        WEBHOOK_URL,
        json={'content': message}
    )


def check_stock():
    resp = requests.get('https://shop.flipperzero.one')
    if resp.status_code != 200:
        send_notification(f'Status Code Error: {resp.status_code}')
        return
    soup = BeautifulSoup(resp.content.decode('utf-8'), 'html.parser')
    results = soup.find_all('script', id=lambda x: x and x.startswith('ProductJson-'))
    if not results:
        send_notification('Unable to find ProductJson')
        return
    data = json.loads(results[0].text)
    if 'available' not in data:
        send_notification('available key missing from ProductJson')
        return
    if data.get('available'):
        send_notification('Product Available!\n\nhttps://shop.flipperzero.one')
        print('Product Available')
        return True
    print('Product Unavailable')
    return False


def main():
    check_stock()


if __name__ == '__main__':
    main()
