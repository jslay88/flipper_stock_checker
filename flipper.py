# Check for stock availability of Flipper Zero
# with optional Discord Webhook Notification
import json
import logging
import os

import requests
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(os.getenv("LOG_LEVEL", logging.INFO))

PRODUCT_URL = os.getenv("PRODUCT_URL", "https://shop.flipperzero.one")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")


def send_notification(message: str):
    print(message)
    # Discord Channel Webhook
    if not WEBHOOK_URL:
        return
    requests.post(WEBHOOK_URL, json={"content": message})


def check_stock():
    resp = requests.get(PRODUCT_URL)
    if resp.status_code != 200:
        send_notification(f"Status Code Error: {resp.status_code}")
        return
    soup = BeautifulSoup(resp.content.decode("utf-8"), "html.parser")
    results = soup.find_all("script", id=lambda x: x and x.startswith("ProductJson-"))
    if not results:
        send_notification("Unable to find ProductJson")
        return
    data = json.loads(results[0].text)
    logger.debug(f"Product Json: {json.dumps(data, indent=2)}")
    if "available" not in data:
        send_notification("available key missing from ProductJson")
        return
    product = data.get("title", "Product")
    if data.get("available"):
        send_notification(f"{product} is Available!\n\n{PRODUCT_URL}")
        return True
    print(f"{product} is Unavailable.\n\n{PRODUCT_URL}")
    return False


def main():
    if not check_stock():
        exit(1)


if __name__ == "__main__":
    main()
