# Creating process and multiprocessing

from multiprocessing import Process
import os
import time


class PrintProcess(Process):
    def __init__(self, name, sec):
        super().__init__()
        self.name = name
        self.sec = sec

    def run(self):
        print("child:", os.getpid())
        print("hello", self.name)
        time.sleep(self.sec)
        print("bye", self.name)
        print("wait", 2*self.sec)
        time.sleep(2*self.sec)
        print("and hello again", self.name)


p = PrintProcess("Mike", 6)
d = PrintProcess("KUZYA", 10)
p.start()
d.start()
print("parent:", os.getpid())
d.join()
p.join()

print("FINISH:", os.getpid())
