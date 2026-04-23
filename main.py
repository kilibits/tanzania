import logging
import time

import lxml.html

from scrapers.education_history import EducationHistory
from scrapers.employment_history import EmploymentHistory
from scrapers.political_career_history import PoliticalCareerHistory
from scrapers.profile_data import ProfileData
from scrapers.term import Term
from scrapers.utils import BASE_URL, fetch_with_retries, save_to_db

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

REQUEST_DELAY = 1.0  # seconds between profile fetches


def parse_members_list(html):
    root = lxml.html.fromstring(html)
    rows = root.cssselect("table.table tbody tr")
    if not rows:
        raise RuntimeError("No member rows found in listing page")
    logger.info("Found %d member rows", len(rows))
    return rows


def scrape():
    education = EducationHistory()
    employment = EmploymentHistory()
    political = PoliticalCareerHistory()

    members = []

    logger.info("Fetching members listing: %s", BASE_URL)
    listing_html = fetch_with_retries(BASE_URL)
    rows = parse_members_list(listing_html)

    for i, row in enumerate(rows, 1):
        profile = ProfileData()
        try:
            profile.add_profile_data(row)
        except (IndexError, AttributeError) as exc:
            logger.warning("Skipping row %d (parse error): %s", i, exc)
            continue

        mp = profile.get_profile()
        logger.info("[%d/%d] %s (%s)", i, len(rows), mp.get("name"), mp.get("id"))

        try:
            member_html = fetch_with_retries(mp["source"])
            member_root = lxml.html.fromstring(member_html)
            profile.add_profile_summary(member_root)
            education.add_education_data(member_root, mp["id"])
            employment.add_employment_data(member_root, mp["id"])
            political.add_political_career_data(member_root, mp["id"])
        except Exception as exc:
            logger.warning("Failed to scrape profile for %s: %s", mp.get("name"), exc)

        members.append(profile.get_profile())
        time.sleep(REQUEST_DELAY)

    logger.info("Saving %d members to database", len(members))
    save_to_db(Term.term_data, "terms", ["id"])
    save_to_db(members, "members", ["id"])
    save_to_db(education.get_education_data(), "education_history", ["id"])
    save_to_db(employment.get_employment_data(), "employment_history", ["id"])
    save_to_db(political.get_political_career_data(), "appointments", ["id"])
    logger.info("Done.")


if __name__ == "__main__":
    scrape()
