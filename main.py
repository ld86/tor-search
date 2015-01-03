import socks
import Queue
import select
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse
import re

# s.connect(('zqktlwi4fecvo6ri.onion', 80))
# s.sendall("GET /wiki/Main_Page/ HTTP/1.1\r\nHost: 3fyb44wdhnd2ghhl.onion\r\n\r\n")


class Crawler:

    def __init__(self):
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050, True)
        self.s = socks.socksocket()
        self.queue = Queue.Queue()

    def serve(self):
        while not self.queue.empty():
            task = self.queue.get()
            self.crawl(task)

    def readall(self, s):
        c = []
        while True:
            r, _, _ = select.select([s], [], [], 10)
            if not r:
                return "".join(c)
            c.append(s.recv(2 ** 16))

    def crawl(self, task):
        s = self.s
        s.connect((task.host, 80))
        s.sendall("GET {0} HTTP/1.1\r\nHost: {1}\r\n\r\n".format(task.path, task.host))
        task.content = self.readall(s)
        s.close()

        self.parse(task)

    def parse(self, task):
        bs = BeautifulSoup(task.content)
        allA = bs.findAll('a', attrs={'href': re.compile(r'\.onion')})
        print("[!] {0} : {1}".format(task.host + task.path, len(allA)))
        for a in allA:
            href = a['href']
            url = urlparse(href)
            print(url)

    def add_task(self, task):
        self.queue.put(task)


class Task:

    def __init__(self, host, path):
        self.host = host
        self.path = path


def main():
    crawler = Crawler()
    crawler.add_task(Task("zqktlwi4fecvo6ri.onion", "/wiki/Main_Page"))
    crawler.serve()


if __name__ == "__main__":
    main()
