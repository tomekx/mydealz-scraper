from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime
from dotenv import load_dotenv
import os


def log(msg):
    now = datetime.now()
    load_dotenv()

    #get timestamp
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    webhook = DiscordWebhook(url=os.getenv('WEBHOOK_URL'))

    embed=DiscordEmbed(title="ERROR", description=msg, color=0xed1a2c)
    embed.set_footer(text=f'{dt_string}  ⋅  mdscrape v0.1')

    webhook.add_embed(embed)

    webhook.execute()

