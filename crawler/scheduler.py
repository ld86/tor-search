from urlparse import urlparse
from time import time, sleep
from Queue import PriorityQueue
from utils.logger import log


class TaskStatuses:
    CREATED = 1


class Task:

    def __init__(self):
        self.created = time()
        self.status = TaskStatuses.CREATED


class Fetch(Task):

    def __init__(self, url):
        self.url = urlparse(url)

    def url(self):
        return self.url.geturl()

    def hostname(self):
        return self.url.netloc()


class Scheduler:

    def __init__(self):
        self.task_queue = PriorityQueue()

    def add_task(self, task):
        self.task_queue(task)

    def start(self):
        while sleep(5) is None:
            log(self.status())
            task = self.task_queue.get()
            print(task)

    def status(self):
        return "{0}".format(self.task_queue.qsize())
