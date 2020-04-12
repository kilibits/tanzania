# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

import re
from urllib.parse import quote as urlquote

import scraperwiki
import lxml.html


def fetch_with_retries(source, max_tries=5):
    tries = 0
    while tries <= max_tries:
        try:
            html = scraperwiki.scrape(source)
            break
        except:
            print("Retrying {}".format(source))
            tries +=1

    return html

def handle_empty_string(text):
    if text:
        return text.strip()
    else:
        return "Missing Data"

# def drop_tables():
#     try:
#         scraperwiki.sqlite.execute("drop table if exists employment_history")
#         scraperwiki.sqlite.execute("drop table if exists education_history")
#         scraperwiki.sqlite.execute("drop table if exists political_experience")
#         scraperwiki.sqlite.commit()
#     except scraperwiki.sqlite.SqliteError, e:
#         print str(e)

def normalize_whitespace(text):
    return re.sub(r'\s+', ' ', text)

source_url = "https://www.bunge.go.tz/polis/members"
term_id = '5'

term_data = [
    {'id': term_id,
     'name': '5th Assembly',
     'start_date': '2015-10-25',
     'source': 'https://en.wikipedia.org/wiki/Tanzanian_parliamentary_election,_2015',
     },
    ]

html = fetch_with_retries(source_url)
root = lxml.html.fromstring(html)
main_table = root.xpath('//table')[0]
summary_table = root.xpath("//table")[1]

main_table_rows = main_table.xpath('.//tbody/tr')

if len(main_table_rows) == 0:
    raise Exception("No rows found in main_table")

data = []
education = []
employment = []
political = []

#used as unique_keys for emloyment, education, and politcal history tables
#incremented for each new record
emp_id = 1
edu_id = 1
pol_id = 1

for row in main_table_rows:
    
    member = {}
    member['term'] = term_id
    member['image'] = urlquote(row.cssselect('img')[0].attrib.get('src')).replace("%3A", ":", 1)
    member['source'] = row.cssselect('a')[0].attrib.get('href')
    member['id'] = member['source'].rsplit('/', 1)[1]

    tds = row.cssselect('td')

    member['name'] = normalize_whitespace(
        re.sub(
            r'^Hon\.\s+',
            '',
            tds[1].cssselect('a')[0].text.strip()
            )
        )

    member['area'] = tds[2].cssselect('a')[0].text.strip()
    member['constituency_src'] = tds[2].cssselect('a')[0].attrib.get('href')
    member['group'] = tds[3].cssselect('a')[0].text.strip()

    max_tries = 5
    tries = 0

    member_html = fetch_with_retries(member['source'])
    member_root = lxml.html.fromstring(member_html)

    profile_summary = member_root.cssselect('div.tr_prof')
    summary_attributes = profile_summary[0].cssselect('div.tr_quick')
    member['sex'] = summary_attributes[0].cssselect('p')[1].text.strip()
    member['contributions'] = summary_attributes[3].cssselect('p')[1].text.strip()
    member['questions'] = summary_attributes[4].cssselect('p')[1].text.strip()
    member['committees'] = summary_attributes[5].cssselect('p')[1].text.strip()

    items = member_root.cssselect('span.item')

    profls = member_root.cssselect('div.profls')
    profile_info = member_root.cssselect('div.tr_info')[0]

    education_div = profile_info.xpath(".//div[@id='education']")[0]
    education_table = education_div.xpath('.//table')[0]
    education_rows = education_table.xpath('.//tbody/tr')

    for e_tr in education_rows:
        e_data = {}
        e_data['id'] = edu_id
        e_data['mp_id'] = member['id']

        e_td = e_tr.cssselect('td')
        e_data['period'] = e_td[0].text.strip()
        e_data['level'] = e_td[1].text.strip()
        e_data['institution'] = e_td[2].text.strip()
        e_data['award'] = e_td[3].text.strip()

        education.append(e_data)
        edu_id += 1

    #training_div = profile_info.xpath(".//div[@id='training']")[0]
    employment_div = profile_info.xpath(".//div[@id='work']")[0]
    employment_table = employment_div.xpath('.//table')[0]
    employment_rows = employment_table.xpath('.//tbody/tr')
    for e_tr in employment_rows:
        e_data = {}
        e_data['id'] = emp_id
        e_data['mp_id'] = member['id']

        e_td = e_tr.cssselect('td')
        e_data['period'] = e_td[0].text.strip()
        e_data['position'] = e_td[1].text.strip()
        e_data['organization'] = e_td[2].text.strip()

        print(e_data)

        employment.append(e_data)
        emp_id += 1

    political_tr = profl_data[2].cssselect('tr.odd')
    for e_tr in political_tr:
        e_data = {}
        e_data['id'] = pol_id
        e_data['mp_id'] = member['id']

        e_td = e_tr.cssselect('td')
        e_data['institution'] = e_td[0].text.strip()
        e_data['position'] = e_td[1].text.strip()
        e_data['from'] = e_td[2].text.strip()
        e_data['to'] = e_td[3].text.strip()

        political.append(e_data)
        pol_id += 1


    item_dict = {}
    for item in items:
        key = re.sub(r'[\s\.]', '', item.text)
        value = item.tail.strip()
        item_dict[key] = value


    member['phone'] = item_dict['Phone:']
    member['email'] = item_dict['EmailAddress:']
    birth_date = item_dict['DateofBirth:']

    # We don't want birth dates of 0000-00-00
    if birth_date != '0000-00-00':
        member['birth_date'] = birth_date
    else:
        member['birth_date'] = 'Missing Data'

    member['member_type'] = item_dict['MemberType:']
    member['address'] = item_dict['POBox:']

    data.append(member)

scraperwiki.sqlite.save(unique_keys=['id'], data=term_data, table_name='terms')
scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name='profile')
scraperwiki.sqlite.save(unique_keys=['id'], data=education, table_name='education_history')
scraperwiki.sqlite.save(unique_keys=['id'], data=employment, table_name='employment_history')
scraperwiki.sqlite.save(unique_keys=['id'], data=political, table_name='political_experience')
