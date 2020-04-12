from scrappers.utils import Utils

class PoliticalCareerHistory:

    def __init__(self):
        self.__political_career = []
        self.__id = 1
    
    def get_political_career_data(self):
        return self.__political_career

    def add_political_career_data(self, political_career_node, member_id):
        for e_tr in political_career_node:
            data = {}
            data['id'] = self.__id
            data['mp_id'] = member_id

            e_td = e_tr.cssselect('td')
            e_data['institution'] = e_td[0].text.strip()
            e_data['position'] = e_td[1].text.strip()
            e_data['from'] = e_td[2].text.strip()
            e_data['to'] = e_td[3].text.strip()

            self.__political_career.append(data)
            self.__id += 1
