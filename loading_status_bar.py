# -*- encoding: utf-8 -*-

import sublime
import threading

class _Loader(threading.Thread):

    def __init__(self, loading_message, final_message):
        super().__init__()
        self.pos = 0
        self.length = 7
        self.loading_message = loading_message
        self.final_message = final_message
        self.going = 1

    def _go(self):
        if self.going == 0:
            return sublime.status_message(self.final_message)

        msg = '['
        msg += ' ' * self.pos
        msg += '='
        msg += ' ' * (self.length - self.pos)
        msg += '] ' + self.loading_message

        msg = '[{}={}] {}'.format(' ' * self.pos, ' ' * (self.length - self.pos), self.loading_message)

        self.pos += self.going
        if self.pos >= self.length:
            self.going = -1
        if self.pos <= 0:
            self.going = 1
        sublime.status_message(msg)
        sublime.set_timeout(self._go, 100)

    def run(self):
        sublime.set_timeout(self._go, 0)

class Loader:

    def go(self, loading_message, final_message):
        self.loader = _Loader(loading_message, final_message)
        self.loader.start()

    def stop(self):
        self.loader.going = 0
        self.loader.join()

loader = Loader()
loader.go('Looking good...', 'Done!')
sublime.set_timeout_async(lambda: loader.stop(), 5000)
