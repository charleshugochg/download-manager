from threading import Thread
from time import time

from terminalsize import get_terminal_size


class OneLinePrinter(Thread):
    def __init__(self, printable, frame_rate=10):
        Thread.__init__(self)
        self.printable = printable
        self.frame_rate = frame_rate
        self.terminal_width, _ = get_terminal_size()

        self.stop = False
        self.setDaemon(True)
        self.start()

    def run(self) -> None:
        last_frame_time = time()
        while not self.stop:
            if time() - last_frame_time > 1/self.frame_rate:
                last_frame_time = time()
                print(self.printable, end='\r')
        print(self.printable, end='\r')
        print()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop = True
        self.join()

    def end(self):
        self.stop = True
        self.join()
