from scrapers.utils import safe_text


class EducationHistory:

    def __init__(self):
        self._education = []
        self._id = 1

    def get_education_data(self):
        return self._education

    def add_education_data(self, member_root, member_id):
        """Parse the education tab.

        Table columns: Year | Level | School | Awards
        """
        section = member_root.cssselect("div#education")
        if not section:
            return
        for tr in section[0].cssselect("tbody tr"):
            tds = tr.cssselect("td")
            if len(tds) < 4:
                continue
            self._education.append({
                "id": str(self._id),
                "mp_id": member_id,
                "year": safe_text(tds[0]),
                "level": safe_text(tds[1]),
                "institution": safe_text(tds[2]),
                "award": safe_text(tds[3]),
            })
            self._id += 1
