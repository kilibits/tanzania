class EducationHistory:

    def __init__(self):
        self.__education = []
        self.__id = 1
    
    def get_education_data(self):
        return self.__education

    def add_education_data(self, education_node, member_id):
        for e_tr in education_node:
            data = {}
            data['id'] = self.__id
            data['mp_id'] = member_id

            e_td = e_tr.cssselect('td')
            data['institution'] = e_td[0].text.strip()
            data['award'] = e_td[1].text.strip()
            data['from'] = e_td[2].text.strip()
            data['to'] = e_td[3].text.strip()
            data['level'] = e_td[4].text.strip()

            self.__education.append(data)
            self.__id += 1
