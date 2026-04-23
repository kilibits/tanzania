import re
import logging
import time
import sqlite3
import urllib3

import requests

# The government site uses a certificate chain that Python's bundled CA store
# cannot verify. Suppress the resulting warnings.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

BASE_URL = "https://polis.bunge.go.tz/members"
DB_PATH = "data.sqlite"

_session = requests.Session()
_session.headers.update({"User-Agent": "tanzania-parliament-scraper/2.0"})
_session.verify = False


def fetch_with_retries(url, max_tries=5):
    for attempt in range(max_tries):
        try:
            resp = _session.get(url, timeout=30)
            resp.raise_for_status()
            return resp.text
        except requests.RequestException as exc:
            logger.warning("Attempt %d/%d failed for %s: %s", attempt + 1, max_tries, url, exc)
            if attempt < max_tries - 1:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"Failed to fetch {url} after {max_tries} attempts")


def normalize_whitespace(text):
    return re.sub(r"\s+", " ", text).strip()


def safe_text(el):
    if el is None:
        return ""
    return normalize_whitespace(el.text_content() if hasattr(el, "text_content") else (el.text or ""))


def save_to_db(data, table_name, unique_keys):
    if not data:
        return
    cols = list(data[0].keys())
    col_defs = ", ".join(
        f"{c} TEXT PRIMARY KEY" if unique_keys == [c] else f"{c} TEXT"
        for c in cols
    )
    if len(unique_keys) > 1:
        col_defs += f", PRIMARY KEY ({', '.join(unique_keys)})"

    placeholders = ", ".join("?" * len(cols))
    col_str = ", ".join(cols)

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({col_defs})")
        for row in data:
            conn.execute(
                f"INSERT OR REPLACE INTO {table_name} ({col_str}) VALUES ({placeholders})",
                [row.get(c, "") for c in cols],
            )
        conn.commit()
    finally:
        conn.close()
