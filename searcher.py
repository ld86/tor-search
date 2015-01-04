from flask import Flask, request, render_template
import pickle
import base64

app = Flask(__name__)


def load(f):
    def u(x):
        return pickle.loads(base64.b64decode(x))
    return map(u, f.read().split('\n')[:-1])


class Searcher:

    def __init__(self):
        with open("arch") as f:
            self.arch = load(f)
        with open("inv") as f:
            self.inv = {}
            for word in load(f):
                self.inv[word['word']] = word['hits']

    def search(self, query):
        words = query.lower().split()
        hits = map(lambda x: self.get_guts(x), words)
        hits.sort(key=lambda x: len(x))
        docs = self.merge(hits)
        return map(lambda x: self.arch[x]['url'], docs)

    def bisect(self, a, b):
        ap = 0
        bp = 0
        result = []
        while ap != len(a) and bp != len(b):
            if a[ap] == b[bp]:
                result.append(a[ap])
                ap += 1
                bp += 1
            elif a[ap] < b[bp]:
                ap += 1
            elif a[ap] > b[bp]:
                bp += 1
        return result

    def merge(self, hits):
        result = hits[0]
        for hit in hits:
            result = self.bisect(result, hit)
        return result

    def get_guts(self, word):
        return self.inv[word] if word in self.inv else []

searcher = Searcher()


@app.route("/")
def index():
    query = request.args.get('q', None)
    result = []
    if query is not None:
        result = searcher.search(query)
    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
