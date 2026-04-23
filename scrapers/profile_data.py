import re

from scrapers.term import Term
from scrapers.utils import normalize_whitespace, safe_text


class ProfileData:

    def __init__(self):
        self._profile = {}

    def get_profile(self):
        return self._profile

    def add_profile_data(self, row):
        """Parse a row from the members listing table."""
        self._profile = {}
        self._profile["term"] = Term.term_id

        tds = row.cssselect("td")
        img = tds[0].cssselect("img")
        self._profile["image"] = img[0].get("src", "") if img else ""

        name_link = tds[1].cssselect("a")[0]
        self._profile["source"] = name_link.get("href", "")
        self._profile["id"] = self._profile["source"].rsplit("/", 1)[-1]
        self._profile["name"] = normalize_whitespace(
            re.sub(r"^(Hon\.|Dr\.|Chief)\s+", "", name_link.text_content()).strip()
        )

        constituency_link = tds[2].cssselect("a")
        if constituency_link:
            self._profile["constituency"] = safe_text(constituency_link[0])
            self._profile["constituency_src"] = constituency_link[0].get("href", "")
        else:
            self._profile["constituency"] = safe_text(tds[2])
            self._profile["constituency_src"] = ""

        party_link = tds[3].cssselect("a")
        self._profile["party"] = safe_text(party_link[0]) if party_link else safe_text(tds[3])

        self._profile["member_type"] = safe_text(tds[4])
        return self._profile

    def add_profile_summary(self, member_root):
        """Parse the tr_quick summary boxes from the member profile page.

        New layout (index): Sex(0) Party(1) Constituent(2)
                            Contributions(3) Questions(4) Answers(5) Committees(6)
        """
        boxes = member_root.cssselect("div.tr_quick")
        def _val(idx):
            if idx < len(boxes):
                p = boxes[idx].cssselect("p.last")
                return safe_text(p[0]) if p else ""
            return ""

        self._profile["sex"] = _val(0)
        self._profile["contributions"] = _val(3)
        self._profile["questions"] = _val(4)
        self._profile["answers"] = _val(5)
        self._profile["committees"] = _val(6)
