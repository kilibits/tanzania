from scrapers.utils import safe_text


class EmploymentHistory:

    def __init__(self):
        self._employment = []
        self._id = 1

    def get_employment_data(self):
        return self._employment

    def add_employment_data(self, member_root, member_id):
        """Parse the work experience tab.

        Table columns: Year | Position | Organization
        """
        section = member_root.cssselect("div#work")
        if not section:
            return
        for tr in section[0].cssselect("tbody tr"):
            tds = tr.cssselect("td")
            if len(tds) < 3:
                continue
            self._employment.append({
                "id": str(self._id),
                "mp_id": member_id,
                "year": safe_text(tds[0]),
                "position": safe_text(tds[1]),
                "organization": safe_text(tds[2]),
            })
            self._id += 1
