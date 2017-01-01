# CSW: ignore
import sublime, sublime_plugin
import sys

class ClearConsoleCommand(sublime_plugin.WindowCommand):

    def run(self):
        # get console size, and font size height, and define the right size
        print('\n' * 30)
