# CSW: ignore
import sublime, sublime_plugin
import sys

class ClearConsoleCommand(sublime_plugin.WindowCommand):

    def run(self):
        print('\n' * 20)
