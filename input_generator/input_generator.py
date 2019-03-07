import json
from os.path import dirname, abspath, join
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class GamerBuddyInputGen(object):

    def __init__(self, product_metadata_file):
        self.metadata_dict = self._load_json_from_file(product_metadata_file)
        # self.review_dict = self._load_json_from_file(product_review_file)
        self.terms_in_file = dict()
        self.term_position = dict()
        self.inverted_index = dict()
        self.product_term_collections = dict()
        self.stop_words = list(set(stopwords.words("english")))

    def _load_json_from_file(self, json_file):
        project_loc = dirname(dirname(abspath(__file__)))
        json_file = join(join(project_loc, "gamerbuddy_dataset"), json_file)
        with open(json_file) as json_obj:
            json_dict = json.load(json_obj)
            print(len(json_dict))
            return json_dict

    def generate_all_terms_in_files(self):
        self._generate_all_terms_in_metadata()
        # self._generate_all_terms_in_review_data()
    def _generate_all_terms_in_metadata(self, ):
        for product in self.metadata_dict:
            self.terms_in_file[product] = self._process_json(self.metadata_dict[product], ["title", "description"])

    def _generate_all_terms_in_review_data(self):
        for asin in self.review_dict:
            for review in self.review_dict[asin]:
                self.terms_in_file[asin][review["reviewerID"]] = self._process_json(review, ["reviewText"])[
                    "reviewText"]

    def generate_complete_inverted_index(self):
        self.generate_all_terms_in_files()
        obj = open("test.json", "w+")
        obj.write(json.dumps(self.terms_in_file))
        self.generate_position_of_terms_in_input_json()

    def _process_json(self, json_dict, key_list):
        json_to_terms = {}
        for key in key_list:
            if key not in json_dict:
                continue
            json_to_terms[key] = [term for term in word_tokenize(json_dict[key].lower(), language="english") if
                                  term not in self.stop_words]
        return json_to_terms

    def _remove_stop_words_from_term_list(self, term_list):
        filtered_term_list = [term for term in term_list if not term in self.stop_words]
        return filtered_term_list

    def generate_position_of_terms_in_input_json(self, file_name=None):
        with open("test.json") as json_obj:
            self.terms_in_file = json.load(json_obj)
            asin_len = len(self.terms_in_file)
            print("asin length :: {}".format(int(asin_len)))
        for count, asin in enumerate(self.terms_in_file, start=1):
            self.product_term_collections[asin] = self._find_all_term_position_for_a_product(self.terms_in_file[asin])
            self._update_term_positions_dictionary(asin, self.product_term_collections)
            print("Asin count {}/{}".format(count, asin_len))
        file_obj = open("inverted_index.json", "w+")
        file_obj2 = open("product_term_collection.json", "w+")
        file_obj.write(json.dumps(self.term_position))
        file_obj2.write(json.dumps(self.product_term_collections))

    def _find_all_term_position_for_a_product(self, product_term_collection):
        term_position = {}
        for key in product_term_collection:
            for index, term in enumerate(product_term_collection[key]):
                if not term in term_position:
                    term_position[term] = {}
                if not key in term_position[term]:
                    term_position[term][key] = []
                term_position[term][key].append(index)
        return term_position

    def _update_term_positions_dictionary(self, asin, term_collection):
        for term in term_collection:
            if not term in self.term_position:
                self.term_position[term] = {}
            if not asin in self.term_position[term]:
                self.term_position[term][asin] = {}
            for key in term_collection[term]:
                self.term_position[term][asin][key] = term_collection[term][key]


# test = {"asin1": {"description": ["hello", "world", "world", "hello", "something"],
#      "title": ["something", "repeating", "hello","hello"],
#      "abcdefgh":["world", "hello", "nothing", "something"]},
#             "asin2":{"description": ["1","2","3", "4", "&", "4",],
#                      "title": ["2", "3", "hi","world", "nothing"],
#                      "wxyz1234": ["hey","nothing"]}}


if __name__ == "__main__":
    GamerBuddyInputGen("product_details.json").generate_complete_inverted_index()#generate_position_of_terms_in_input_json()

    # GamerBuddyInputGen("meta_Video_Games.json", "reviews_Video_Games.json").generate_position_of_terms_in_input_json()
