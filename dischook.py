from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime
from dotenv import load_dotenv
import os

from logger import get_module_logger



def send_hook(title, href, price, discount, img, med_price, sales_week, sales_month, sales_total, ebay_url):
    now = datetime.now()
    load_dotenv()

    #check if deal is voucher
    if price == None:
        price = 'None'

    #get timestamp
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    try:

        #init webhook
        webhook = DiscordWebhook(url=os.getenv('WEBHOOK_URL'))

        #customize webhook
        embed=DiscordEmbed(title="New Result", url=href, description=title, color=0x007036)
        embed.set_author(name="mdscrape", url="https://static.mydealz.de/threads/raw/SpBKh/2117884_1/re/300x300/qt/60/2117884_1.jpg", icon_url="https://i.imgur.com/YJhsxtg_d.webp?maxwidth=760&fidelity=grand")
        embed.set_thumbnail(url=img)
        embed.add_embed_field(name="Price", value=price, inline=True)
        embed.add_embed_field(name="Discount", value=discount, inline=True)
        embed.add_embed_field(name="Avg. price", value=med_price, inline=False)
        embed.add_embed_field(name="Weekly sales", value=sales_week, inline=True)
        embed.add_embed_field(name="Monthly sales", value=sales_month, inline=True)
        embed.add_embed_field(name="Total sales", value=sales_total, inline=True)
        embed.add_embed_field(name="Ebay Url", value=f"[Link]({ebay_url})", inline=True)
        embed.set_footer(text=f'{dt_string}  ⋅  mdscrape v0.1')

        #send webhook
        webhook.add_embed(embed)

        webhook.execute()

    except:
        get_module_logger('dischook').info(f'Error occured on deal {title} ---- {href}')