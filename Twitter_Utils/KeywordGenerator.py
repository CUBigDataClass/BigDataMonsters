import os
import simplejson as json
import logging


class KeywordGenerator:
    def __init__(self):
        wd = os.getcwd()
        pos = wd.find("BigDataMonsters")
        if pos > 0:  # pragma: no cover
            path = wd[0:pos+15]
        else:
            path = wd
        self.team_data_path = path + '/Twitter_Utils/data/teams-data.json'
        self.logger = logging.getLogger(__name__)

    def generate_search_terms(self, team_id):
        """
        Creates list of key words to search for.
        :param team_id: id of team, given by Stattleship API
        :return: returns list of key words
        """
        try:
            with open(self.team_data_path, 'r') as f:
                data = json.loads(f.read())
            f.close()

            search_terms_list = []
            team_data = data['teams']
            for team in team_data:
                if team['id'] == team_id:
                    if team['hashtag']:
                        search_terms_list.append(team['hashtag'])

                    for hashtag in team['hashtags']:
                        search_terms_list.append(hashtag)

                    if team['nickname']:
                        search_terms_list.append(team['nickname'])
                    # if team['name']:
                    #     search_terms_list.append(team['name'])

            search_terms_list = self.append_word_with_go_to_list(search_terms_list)
            return search_terms_list

        except IOError:
            self.logger.exception(IOError)
            self.logger.error('Search terms not found at ' + self.team_data_path)
            raise IOError

    @staticmethod
    def append_word_with_go_to_list(word_list):
        # TODO - Refactor this
        search_terms_list_with_go = []
        for word in word_list:
            search_terms_list_with_go.append('go' + word)

        word_list += search_terms_list_with_go
        return word_list
