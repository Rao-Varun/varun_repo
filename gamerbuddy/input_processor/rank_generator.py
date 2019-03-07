from math import sqrt


class RankGenerator(object):

    def __init__(self, tf_details, idf_details):
        self.tf_details = tf_details
        self.idf_details = idf_details
        self.product_list = None
        self.query_words_list = None

    def generate_ranks_for_products(self, query_words_list, product_list):
        product_tf_idf = self._generate_tf_idf_value_for_products(product_list, query_words_list)
        query_tf_idf = self._generate_tf_idf_value_for_query(query_words_list)
        sorted_products = sorted(self._generate_cosine_value(product_tf_idf, query_tf_idf).items(),
                                 key=lambda kv: kv[1], reverse=True)
        return [product_det[0] for product_det in sorted_products]

    def _generate_tf_idf_value_for_products(self, product_list, query_words_list):
        print("info :: generating tf-idf value for products...")
        product_tf_idf = self._generate_tf_idf_without_normalization(product_list, query_words_list)
        return self._nomalise_tf_idf(product_tf_idf)

    def _generate_tf_idf_without_normalization(self, product_list, query_words_list):
        print("info :: generate tf-id without normalization...")
        product_tf_idf = dict()
        for asin in product_list:
            product_tf_idf[asin] = {}
            for term in query_words_list:
                tf = self.tf_details[term][asin]
                idf = self.idf_details[term]
                product_tf_idf[asin][term] = tf * idf
        print("unnormalised")
        print(product_tf_idf)
        return product_tf_idf

    def _nomalise_tf_idf(self, product_tf_idf):
        print("info :: normalise tf-idf...")
        for product in product_tf_idf:
            temp_product = product_tf_idf[product]
            magnitude = sqrt(sum([temp_product[term] ** 2 for term in temp_product]))
            print("magnitude {}".format(str(magnitude)))
            for term in temp_product:
                temp_product[term] /= magnitude
        print(product_tf_idf)
        return product_tf_idf

    def _generate_tf_idf_value_for_query(self, query_words_list):
        print("info :: generating tf-idf value for query...")
        query_tf_idf = self.generate_unnormalized_tf_idf_for_query(query_words_list)
        return self.normalize_tf_idf_for_query(query_tf_idf)

    def generate_unnormalized_tf_idf_for_query(self, query_words_list):
        print("info :: generating unnormalised tf-idf value for query...")
        query_tf_idf = dict()
        total_len = 0
        for term in query_words_list:
            total_len += len(query_words_list[term])
        for term in query_words_list:
            tf = float(sum(query_words_list[term])) / total_len
            idf = float(self.idf_details[term])
            query_tf_idf[term] = tf * idf
        return query_tf_idf

    def normalize_tf_idf_for_query(self, query_tf_idf):
        print("info :: generating tf-idf for query...")
        magnitude = sqrt(sum([query_tf_idf[term] ** 2 for term in query_tf_idf]))
        for term in query_tf_idf:
            query_tf_idf[term] /= magnitude
        print("query tf-idf {}".format(str(query_tf_idf)))
        return query_tf_idf

    def _generate_cosine_value(self, product_tf_idf, query_tf_idf):
        print("info :: generating cosine values")
        product_rank = dict()
        for product in product_tf_idf:
            temp_product = product_tf_idf[product]
            for term in query_tf_idf:
                product_rank[product] = temp_product[term] * query_tf_idf[term]
        print("info :: cosine result {}.....".format(str(product_rank)))
        return product_rank
