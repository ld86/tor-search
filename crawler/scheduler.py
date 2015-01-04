from urlparse import urlparse
from time import time, sleep
from Queue import Queue
from threading import Thread
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


class Scheduler(Thread):

    def __init__(self):
        super(Scheduler, self).__init__()
        self.task_queue = Queue()

    def add_task(self, task):
        self.task_queue(task)

    def run(self):
        while True:
            log("Hello")
            sleep(5)
