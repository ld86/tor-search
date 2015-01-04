import sqlite3
import sys
from BeautifulSoup import BeautifulSoup
import re
# from urlparse import urlparse
import pickle
import base64


def hrefs(cursor):
    for row in cursor.execute("select * from contents;"):
        yield row[0]


def log(frmt, content):
    sys.stderr.write(frmt.format(content))
    sys.stderr.write("\n")


class Archive:

    def __init__(self, filename):
        self.f = open(filename, 'wb')
        self.line = 0

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.f.close()

    def add(self, document):
        doc = {"id": self.line, "url": document.host}
        self.f.write(base64.b64encode(pickle.dumps(doc)))
        self.f.write("\n")
        self.line += 1
        return self.line - 1


class Inverted:

    def __init__(self, filename):
        self.f = open(filename, 'wb')
        self.index = {}

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.write_to_file()
        self.f.close()

    def write_to_file(self):
        keys = sorted(self.index.keys())
        for key in keys:
            doc = {"word": key, "hits": sorted(self.index[key])}
            self.f.write(base64.b64encode(pickle.dumps(doc)))
            self.f.write("\n")

    def add(self, doc_id, content):
        content = re.sub(r'\W', " ", " ".join(content))
        for word in content.lower().split():
            if word in self.index:
                self.index[word].append(doc_id)
            else:
                self.index[word] = [doc_id]


class Indexer:

    def __init__(self, db_filename, table):
        self.db = sqlite3.connect(db_filename)
        self.table = table

    def start(self):
        cursor = self.db.cursor()
        counter = 0
        with Archive("arch") as sa, Inverted("inv") as inv:
            for row in cursor.execute("select * from {0}".format(self.table)):
                self.process(sa, inv, Document(*row))
                counter += 1
                if counter % 10 == 0:
                    log("{0}", (counter))

    def process(self, sa, inv, document):
            doc_id = sa.add(document)
            inv.add(doc_id, [document.title])


class Document:

    def __init__(self, host, ts, content):
        self.host = host
        self.ts = ts
        self.content = content
        self.fill_fields()

    def fill_fields(self):
        bs = BeautifulSoup(self.content)
        allA = bs.findAll('a', attrs={'href': re.compile(r'\.onion')})
        self.title = bs.title.string if bs.title and bs.title.string else ''
        self.links = ((a['href'], a.contents) for a in allA)


def main(db_filename):
    indexer = Indexer(db_filename, "contents")
    indexer.start()


if __name__ == "__main__":
    main(sys.argv[1])
