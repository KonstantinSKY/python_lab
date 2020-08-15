# Creating process Python

import time
import os

foo = "bar"
pid = os.fork()
if pid == 0:
    # child process
    count = 0
    while True:
        print(count)
        print("child:", os.getpid())
        time.sleep(5)
        count += 1
        if count > 15:
            foo = "baz"
            print("child:", foo)
            break

else:
    # parent process
    print("parent:", os.getpid())
    print("parent:", foo)
    time.sleep(10)
    print(os.wait())
    print("FINISH:", os.getpid())

