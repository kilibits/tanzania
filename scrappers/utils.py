# This code is derived from Python scraper on morph.io (https://morph.io)
import re
from urllib.parse import quote as urlquote
import scraperwiki
import lxml.html


class Utils:

    base_url = "https://www.bunge.go.tz/polis/members"

    def __init__(self):
        pass

    @staticmethod
    def fetch_with_retries(source, max_tries=5):
        tries = 0
        while tries <= max_tries:
            try:
                html = scraperwiki.scrape(source)
                break
            except:
                print("Retrying {}".format(source))
                tries += 1

        return html

    @staticmethod
    def handle_empty_string(text):
        if text:
            return text.strip()
        else:
            return "Missing Data"

    @staticmethod
    def normalize_whitespace(text):
        return re.sub(r'\s+', ' ', text)

    @staticmethod
    def save(data, table_name, keys=['id']):
        scraperwiki.sqlite.save(unique_keys=keys, table_name=table_name, data=data)

    @staticmethod
    def decode_url(url):
        return urlquote(url).replace("%3A", ":", 1)

