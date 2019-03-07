import json
from os.path import dirname, abspath, join
from math import log


class Tf_Idf(object):

    def __init__(self):
        self.product_details = self._load_json_from_file("test.json")
        self.inverse_index = self._load_json_from_file("inverted_index.json")
        self.total_number_of_product = float(len(self.product_details))
        self.product_length = dict()
        self.term_tf = dict()
        self.term_idf = dict()

    def _load_json_from_file(self, json_file):
        print("loading json file {} ...".format(json_file))
        project_loc = dirname(dirname(abspath(__file__)))
        json_file = join(join(project_loc, "input_generator"), json_file)
        with open(json_file) as json_obj:
            json_dict = json.load(json_obj)
            print(len(json_dict))
            return json_dict

    def generate_tf_and_idf_attributes(self):
        self._generate_tf_for_terms_in_all_products()
        self._generate_idf_for_terms()
        self._write_tf_idf_values_to_resp_files()

    def _generate_tf_for_terms_in_all_products(self):
        print("info :: generating tf for terms...")
        total_len = len(self.inverse_index)
        for count, term in enumerate(self.inverse_index, start=1):
            self.term_tf[term] = dict()
            print("info :: {}/{} {}".format(count, total_len, term))
            for product in self.inverse_index[term]:
                term_count = self._get_term_count_in_a_product(term, product)
                all_term_count = self._get_all_term_count_in_product(product)
                self._generate_tf_value_of_a_term_for_a_product(term, product, term_count, all_term_count)

    def _get_term_count_in_a_product(self, term, product):
        inv_ind_dict = self.inverse_index[term][product]
        term_count = sum([len(inv_ind_dict[key]) for key in inv_ind_dict])
        # print(term_count)
        return term_count

    def _get_all_term_count_in_product(self, product):
        # print("info :: generating all term count in {}".format(product))
        if product in self.product_length:
            return self.product_length[product]
        product_details = self.product_details[product]
        result = sum([len(product_details[key]) for key in product_details])
        # print(result)
        self.product_length[product] = result
        return result

    def _generate_tf_value_of_a_term_for_a_product(self, term, product, term_count, all_term_count):
        # print("info :: generate tf value for term {}".format(term))
        self.term_tf[term][product] = float(term_count) / float(all_term_count)

    def _generate_idf_for_terms(self):
        print("info :: generating idf for terms")
        total_len = len(self.inverse_index)
        for count, term in enumerate(self.inverse_index, start=1):
            print("info :: {}/{} {}".format(count, total_len, term))
            term_document_count = len(self.inverse_index[term].keys())
            self.term_idf[term] = 1 + log(self.total_number_of_product / float(term_document_count))

    def _write_tf_idf_values_to_resp_files(self):
        print("info :: writing tf and idf values in respective files  ")
        tf_file = open("term_frequency.json", "w+")
        idf_file = open("inverse_document_frequency.json", "w+")
        tf_file.write(json.dumps(self.term_tf))
        idf_file.write(json.dumps(self.term_idf))
        tf_file.close()
        idf_file.close()


if __name__ == "__main__":
    Tf_Idf().generate_tf_and_idf_attributes()
