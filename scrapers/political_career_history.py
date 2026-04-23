from scrapers.utils import safe_text

# Map of tab id → human-readable appointment type
APPOINTMENT_TYPES = {
    "app_type_1": "Ministry",
    "app_type_3": "Committee",
    "app_type_5": "Political Institution",
    "app_type_7": "Other Institution",
}


class PoliticalCareerHistory:

    def __init__(self):
        self._appointments = []
        self._id = 1

    def get_political_career_data(self):
        return self._appointments

    def add_political_career_data(self, member_root, member_id):
        """Parse all appointment tabs (ministries, committees, political, other).

        Table columns: # | Duration | Position | Name
        """
        for tab_id, appt_type in APPOINTMENT_TYPES.items():
            section = member_root.cssselect(f"div#{tab_id}")
            if not section:
                continue
            for tr in section[0].cssselect("tbody tr"):
                tds = tr.cssselect("td")
                if len(tds) < 4:
                    continue
                self._appointments.append({
                    "id": str(self._id),
                    "mp_id": member_id,
                    "type": appt_type,
                    "duration": safe_text(tds[1]),
                    "position": safe_text(tds[2]),
                    "institution": safe_text(tds[3]),
                })
                self._id += 1
