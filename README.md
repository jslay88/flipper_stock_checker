# Flipper Zero Stock Checker

[![Flipper Zero Stock](https://github.com/jslay88/flipper_stock_checker/actions/workflows/check_stock.yml/badge.svg?event=schedule)](https://shop.flipperzero.one)
[![WiFi Devboard for Flipper Zero Stock](https://github.com/jslay88/flipper_stock_checker/actions/workflows/check_wifi_stock.yml/badge.svg?event=schedule)](https://shop.flipperzero.one/products/wifi-devboard)

Badge represents current Flipper Zero Stock on the 
[official shop](https://shop.flipperzero.one). 
Runs every 5 minutes (or as GitHub sees fit).

You can also [fork this repository](https://github.com/jslay88/flipper_stock_checker/fork)
and add a `WEBHOOK_URL` Actions secret, containing a 
[Discord Channel Webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)
for notifications. **Note** this does not use the `/github` 
part of Discord Webhook URLs
