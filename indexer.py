import sqlite3
import sys
from BeautifulSoup import BeautifulSoup
import re
from urlparse import urlparse


def hrefs(cursor):
    for row in cursor.execute("select * from contents;"):
        yield row[0]


def log(frmt, content):
    sys.stderr.write(frmt.format(content))
    sys.stderr.write("\n")


class SearchArchive:
    pass


class Indexer:

    def __init__(self, db_filename, table):
        self.db = sqlite3.connect(db_filename)
        self.table = table

    def start(self):
        cursor = self.db.cursor()
        counter = 0
        for row in cursor.execute("select * from {0}".format(self.table)):
            self.process(Document(*row))
            counter += 1
            if counter % 10 == 0:
                log("{0}", (counter))
                break

    def process(sefl, document):
        host = urlparse(document.host)
        print(document.title)
        print(host)
        for link in document.links:
            print(urlparse(link[0]))


class Document:

    def __init__(self, host, ts, content):
        self.host = host
        self.ts = ts
        self.content = content
        self.fill_fields()

    def fill_fields(self):
        bs = BeautifulSoup(self.content)
        allA = bs.findAll('a', attrs={'href': re.compile(r'\.onion')})
        self.title = bs.title.string if bs.title else ''
        self.links = ((a['href'], a.contents) for a in allA)


def main(db_filename):
    indexer = Indexer(db_filename, "contents")
    indexer.start()


if __name__ == "__main__":
    main(sys.argv[1])
