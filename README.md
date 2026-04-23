# Tanzania Parliament Scraper

Scrapes member profiles from the Tanzania Parliament POLIS system at [polis.bunge.go.tz/members](https://polis.bunge.go.tz/members) and stores the data in a local SQLite database.

Originally based on [everypolitician-scrapers/tanzania](https://github.com/everypolitician-scrapers/tanzania).

## Data collected

| Table | Description |
|---|---|
| `terms` | Parliament term metadata |
| `members` | MP profiles: name, party, constituency, sex, contributions, questions, answers, committees |
| `education_history` | Education background per MP |
| `employment_history` | Work experience per MP |
| `appointments` | Ministerial, committee, political and other institutional appointments per MP |

## Requirements

- Python 3.11+

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python3 main.py
```

Output is written to `data.sqlite` in the project root.

## Notes

- The POLIS site uses a certificate chain that is not in Python's default CA bundle. SSL verification is disabled automatically — this is expected for this government host.
- Requests are rate-limited to 1 second between profile fetches to avoid overloading the server.
- All 433+ member rows load on a single page (DataTables handles client-side filtering), so no pagination is needed.
