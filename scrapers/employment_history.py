from scrapers.utils import Utils

class EmploymentHistory:

    def __init__(self):
        self.__employment = []
        self.__id = 1
    
    def get_employment_data(self):
        return self.__employment

    def add_employment_data(self, employment_node, member_id):
        for e_tr in employment_node:
            data = {}
            data['id'] = self.__id
            data['mp_id'] = member_id

            e_td = e_tr.cssselect('td')
            data['institution'] = e_td[0].text.strip()
            data['position'] = Utils.handle_empty_string(e_td[1].text) #workaround for blanks in some MP profiles
            data['from'] = e_td[2].text.strip()
            data['to'] = e_td[3].text.strip()

            self.__employment.append(data)
            self.__id += 1
