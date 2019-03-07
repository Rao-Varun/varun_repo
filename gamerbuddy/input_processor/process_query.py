import json
from os.path import dirname, abspath, join
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class ProcessQuery(object):

    def __init__(self, product_details, inverted_index):
        self.product_details = product_details
        self.inverted_index = inverted_index
        self.stop_words = list(set(stopwords.words("english")))

    def _load_json_from_file(self, json_file):
        print("info :: loading inverted_index...")
        project_loc = dirname(dirname(abspath(__file__)))
        json_file = join(join(project_loc, "gamerbuddy_inputs"), json_file)
        with open(json_file) as json_obj:
            return json.load(json_obj)

    def _get_query_words(self, query):
        print("info :: splitting query sentence...")
        return [term for term in word_tokenize(query.lower(), language="english") if
                term not in self.stop_words]

    def process_query(self, query):
        print("info :: begin processing query...")
        self.query_list = self._get_query_words(query)
        print("info :: query list - {}".format(str(self.query_list)))
        term_asin_list = self._get_asin_from_inverted_index()
        common_asin_list = self._get_common_asin_products(term_asin_list)
        return self._get_asin_containing_query(common_asin_list)
        # common_asin_key_list = self._get_asin_containing_query(common_asin_list)
        # exact_assin = self._get_position_of_query_words(common_asin_key_list)
        # return self._get_matching_asin(exact_assin)

    def _get_asin_from_inverted_index(self):
        print("info :: obtaining inverted index...")
        term_asin_list = {}
        for term in self.query_list:
            term_asin_list[term] = self.inverted_index.get(term)
        return term_asin_list

    def _get_common_asin_products(self, term_asin_list):
        print("info :: getting products(asin) containing all term words...")
        common_asin = set()
        for term in term_asin_list:
            print("term :: {}....".format(str(term)))
            if len(common_asin) == 0:
                common_asin = set(term_asin_list[term].keys())
            else:
                common_asin = common_asin & set(term_asin_list[term].keys())
        return list(common_asin)

    def _get_asin_containing_query(self, common_asin_list):
        print("info :: getting keys for products that common for all terms.....")
        common_keys_for_asin = {}
        for asin in common_asin_list:
            for term in set(self.query_list):
                if asin not in common_keys_for_asin:
                    common_keys_for_asin[asin] = set(self.inverted_index[term][asin].keys())
                else:
                    common_keys_for_asin[asin] = common_keys_for_asin[asin] & set(
                        self.inverted_index[term][asin].keys())
            common_keys_for_asin[asin] = list(common_keys_for_asin[asin])
        return common_keys_for_asin

    def _get_position_of_query_words(self, common_asin_list):
        asin_result_list = {}
        for asin in common_asin_list:
            common_asin_list[asin] = {}
            for key in common_asin_list[asin]:
                common_asin_list[asin][key] = set()
                for count, term in enumerate(self.query_list):
                    temp_list = set([pos - count for count, pos in enumerate(self.inverted_index[term][asin][key])])
                    if len(asin_result_list[asin][key]) == 0:
                        asin_result_list[asin][key] = temp_list
                    else:
                        asin_result_list[asin][key] = asin_result_list[asin][key] & temp_list
                asin_result_list[asin][key] = list(asin_result_list[asin][key])
        return asin_result_list

    def _get_matching_asin(self, asin_list):
        result_list = []
        for asin in asin_list:
            for key in asin_list:
                if len(asin_list[asin][key]) > 0:
                    result_list.append(asin)
                    break
        return result_list
