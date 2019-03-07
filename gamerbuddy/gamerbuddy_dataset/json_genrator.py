import json
import gzip

def parse(path):
  g = gzip.open(path, 'r')
  for l in g:
    yield json.dumps(eval(l))


if __name__ == "__main__":
    path = input("Enter .zip path: \n")
    final_path = path.replace(".gz", "")
    f = open(final_path, 'w+')
    s = []
    for l in parse(path):
        s .append(l)
    f.write("[\n{}\n]".format(",\n".join(s)))
    f.close()
