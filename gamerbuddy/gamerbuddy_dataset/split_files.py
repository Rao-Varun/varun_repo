import json
def split_file(file_name):
    product_dict = {}
    input_file = open(file_name+".json", "r+")
    output_file = open("product_details.json", "w+")
    input_json = json.loads(input_file.read())
    print("length of input :: {} ".format(len(input_json)))
    half_len = int(len(input_json)/2)
    output_json = input_json[:half_len]
    for product in output_json:
        product_dict[product["asin"]] = product
        del(product["asin"])
    print(len(product_dict))
    output_file.write(json.dumps(product_dict, sort_keys=True, indent=4))
    output_file.close()

def split_file_review(file_name):
    review_dict = {}
    input_file = open(file_name + ".json", "r+")
    output_file = open("product_reviews.json", "w+")
    meta_file = open("product_details.json", "r+")
    input_json = json.loads(input_file.read())
    meta_json = json.loads(meta_file.read())
    products = meta_json.keys()
    for review in input_json:
        if review["asin"] in products:
            if review["asin"] not in review_dict:
                review_dict[review["asin"]] = [review]
            else:
                review_dict[review["asin"]].append(review)
        del (review["asin"])
    output_file.write(json.dumps(review_dict, sort_keys=True, indent=4))
    output_file.close()



if __name__ == "__main__":
    split_file("meta_Video_Games")
    split_file_review("reviews_Video_Games")
