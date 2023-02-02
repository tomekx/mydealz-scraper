from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime
from dotenv import load_dotenv
import os

from logger import log

class DiscHook:
    def __init__(self, title, href, price, discount, img, med_price, sales_week, sales_month, sales_total, ebay_url):
        self.title = title
        self.href = href
        self.price = price
        self.discount = discount
        self.img = img
        self.med_price = med_price
        self.sales_week = sales_week
        self.sales_month = sales_month
        self.sales_total = sales_total
        self.ebay_url = ebay_url

    def send_hook(self):
        now = datetime.now()
        load_dotenv()

        #check if deal is voucher
        if self.price == None:
            self.price = 'None'

        #get timestamp
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        try:

            #init webhook
            webhook = DiscordWebhook(url=os.getenv('WEBHOOK_URL'))

            #customize webhook
            embed=DiscordEmbed(title="New Result", url=self.href, description=self.title, color=0x007036)
            embed.set_author(name="mdscrape", url="https://static.mydealz.de/threads/raw/SpBKh/2117884_1/re/300x300/qt/60/2117884_1.jpg", icon_url="https://i.imgur.com/YJhsxtg_d.webp?maxwidth=760&fidelity=grand")
            embed.set_thumbnail(url=self.img)
            embed.add_embed_field(name="Price", value=self.price, inline=True)
            embed.add_embed_field(name="Discount", value=self.discount, inline=True)
            embed.add_embed_field(name="Avg. price", value=self.med_price, inline=False)
            embed.add_embed_field(name="Weekly sales", value=self.sales_week, inline=True)
            embed.add_embed_field(name="Monthly sales", value=self.sales_month, inline=True)
            embed.add_embed_field(name="Total sales", value=self.sales_total, inline=True)
            embed.add_embed_field(name="Ebay Url", value=f"[Link]({self.ebay_url})", inline=True)
            embed.set_footer(text=f'{dt_string}  ⋅  mdscrape v0.1')

            #send webhook
            webhook.add_embed(embed)

            webhook.execute()

        except:
            log(f'Error occured on deal {self.title} ---- {self.href}')