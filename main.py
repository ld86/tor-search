import socks
import socket


def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    address = (address[0].encode('utf-8'), address[1])
    sock.connect(address)
    return sock

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
socket.socket = socks.socksocket
socket.create_connection = create_connection

import Queue
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse
import re
import urllib2


class Crawler:

    def __init__(self):
        self.queue = Queue.Queue()
        self.was = set()

    def serve(self):
        while not self.queue.empty():
            task = self.queue.get()
            self.crawl(task)

    def crawl(self, task):
        if task.url() in self.was or not task.scheme.startswith("http"):
            return
        self.was.add(task.url())

        print("[>] {0}".format(task.url()))
        try:

            task.content = urllib2.urlopen(task.url())
        except socks.GeneralProxyError as e:
            print("[!] {0} : {1}".format(task.url(), e))
            return
        self.parse(task)

    def parse(self, task):
        bs = BeautifulSoup(task.content)
        allA = bs.findAll('a', attrs={'href': re.compile(r'\.onion')})
        print("[<] {0} : {1}".format(task.url(), len(allA)))
        for a in allA:
            href = a['href']
            self.queue.put(Task(href))

    def add_task(self, task):
        self.queue.put(task)


class Task:

    def __init__(self, url):
        url = urlparse(url)
        self.scheme = url.scheme + "://"
        self.host = url.netloc
        self.path = '/' if url.path == '' else url.path

    def url(self):
        return self.scheme + self.host + self.path


def main():
    crawler = Crawler()
    crawler.add_task(Task("http://zqktlwi4fecvo6ri.onion/wiki/Main_Page"))
    # crawler.add_task(Task("http://cyjabr4pfzupo7pg.onion/"))
    crawler.serve()


if __name__ == "__main__":
    main()
