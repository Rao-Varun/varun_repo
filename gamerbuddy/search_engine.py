from input_processor.process_query import ProcessQuery
from input_processor.rank_generator import RankGenerator
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class SearchEngine(object):

    def __init__(self):
        self.product_details = self._get_product_details("gamerbuddy_dataset/product_details.json")
        self.review_details = self._get_product_details("gamerbuddy_dataset/product_reviews.json")
        self.inverted_index = self._get_product_details("input_generator/inverted_index.json")
        self.tf_detail = self._get_product_details("input_generator/term_frequency.json")
        self.idf_details = self._get_product_details("input_generator/inverse_document_frequency.json")
        self.stop_words = list(set(stopwords.words("english")))
        self.query_processor = ProcessQuery(product_details=self.product_details, inverted_index=self.inverted_index)
        self.rank_generator = RankGenerator(tf_details=self.tf_detail, idf_details=self.idf_details)

    def _get_product_details(self, json_file):
        print("info :: loading {}...".format(json_file))
        with open(json_file) as json_obj:
            return json.load(json_obj)

    def search_product_in_dataset(self, query):
        query_term_list = self._get_query_terms(query)
        product_list = self.query_processor.process_query(query)
        print("query words present in the following document {}".format(str(product_list)))
        query_index = self._get_query_index(query_term_list)
        result = self.rank_generator.generate_ranks_for_products(query_index, product_list)
        print(result)

    def _get_query_index(self, query_terms_list):
        query_words_index = {}
        for index, term in enumerate(query_terms_list, start=1):
            if term not in query_words_index:
                query_words_index[term] = [index]
            else:
                query_words_index[term].append(index)
        return query_words_index

    def _get_query_terms(self, query):
        print(query)
        return [term for term in word_tokenize(query.lower(), language="english") if
                term not in self.stop_words]

if __name__ == "__main__":
    query = ""
    while(True):
        query = input("Enter query \n")
        if query == "exit":
            exit()
        SearchEngine().search_product_in_dataset(query)
