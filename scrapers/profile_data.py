import re
from scrapers.term import Term;
from scrapers.utils import Utils;
class ProfileData:

    def __init__(self):
        self.__profile = {}
        pass

    def get_profile(self):
        return self.__profile

    def add_profile_data(self, base_profile_node):
        self.__profile = {}
        self.__profile['term'] = Term.term_id
        self.__profile['image'] = Utils.decode_url(base_profile_node.cssselect('img')[0].attrib.get('src'))
        self.__profile['source'] = base_profile_node.cssselect('a')[0].attrib.get('href')
        self.__profile['id'] = self.__profile['source'].rsplit('/', 1)[1]

        tds = base_profile_node.cssselect('td')

        self.__profile['name'] = Utils.normalize_whitespace(
        re.sub(
            r'^Hon\.\s+',
            '',
            tds[1].cssselect('a')[0].text.strip()
            )
        )

        self.__profile['area'] = tds[2].cssselect('a')[0].text.strip()
        self.__profile['constituency_src'] = tds[2].cssselect('a')[0].attrib.get('href')
        self.__profile['group'] = tds[3].cssselect('a')[0].text.strip()

        return self.__profile

    def add_profile_summary(self, summary_attributes_node):
        self.__profile['sex'] = summary_attributes_node[0].cssselect('p')[1].text.strip()
        self.__profile['contributions'] = summary_attributes_node[3].cssselect('p')[1].text.strip()
        self.__profile['questions'] = summary_attributes_node[4].cssselect('p')[1].text.strip()
        self.__profile['committees'] = summary_attributes_node[5].cssselect('p')[1].text.strip()