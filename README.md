# Amazon-products-scraping
Amazon products scraping using Python

A simple and scraping script for amazon products. It writes result in a Json file
It use proxy rotation and lots of sleeps between retries to avoid being banned.
This script is strictly for "study only" as scraping is not allowed by Amazon terms and conditions.

It first check the free available proxies from https://free-proxy-list.net/
Then check if the proxy is working.
Finally it try to scrape under that proxy.

# USAGE
simply update with your data this variable:
- "asinlist" 
  with your ASIN codes list
- "locurl"
  with the local marketplace you want to use (amazon.de, amazon.fr, etc)

Then simply run "python amazon_scraping.py"
A json file will be created (data_scrap_amz.json)
  
Enjoy.
