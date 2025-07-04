import curses
import queue
import time

class CursesDrawer:
    def __init__(self):
        self.stdscr = None
        self.draw_queue = queue.Queue()

    def start(self):
        curses.wrapper(self._main)

    def _main(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        self.stdscr.clear()
        self.stdscr.refresh()
        self.loop()

    def draw(self, text):
        self.draw_queue.put(text)

    def loop(self):
        while True:
            if not self.draw_queue.empty():
                text = self.draw_queue.get()
                self.stdscr.clear()
                self.stdscr.addstr(0, 0, text)
                self.stdscr.refresh()
            time.sleep(0.05) 
