# mydealz-scraper
 Script for scraping mydealz website and comparing deals with sold items on ebay to evaluate if there is possible profit.

**Step 1:**
Add OpenAI API Key and Discord Webhook in .env file

**Step 2:**
Send a POST request to *http://127.0.0.1:5000/config* with a JSON body in this format:
```
{
    "pages": 4, # number of pages to be scraped
    "subpage": "new", # new or hot is possible
    "voucher": false, # if the bot should pickup vouchers or only deals
    "min_price": 0,
    "max_price": 1000000,
    "keywords": ["add", "keywords", "in", "array"],
    "blacklist": ["add", "blacklisted", "keywords", "in", "array"]
}
```
**The script starts automatically!**