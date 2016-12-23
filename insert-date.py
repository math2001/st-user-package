import sublime, sublime_plugin
import os
import time

def md(*t):
	t = ' '.join([str(el) for el in t])
	return sublime.message_dialog(t)

def sm(*t):
	t = ' '.join([str(el) for el in t])
	return sublime.status_message(t)

def em(*t):
	t = ' '.join([str(el) for el in t])
	return sublime.error_message(t)

def string(*text, **kwargs):
	return kwargs.get('sep', ' ').join([str(t) for t in text])

class WriteDateCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		self.window = self.view.window()
		self.selection = sublime.Selection(self.view.id())
		self.settings = self.view.settings()
		today = time.localtime()
		days = [
			'Monday',
			'Tuesday',
			'Wednesday',
			'Thursday',
			'Friday',
			'Saturday',
			'Sunday'
		]
		months = [
			'January',
			'February',
			'Mars',
			'April',
			'May',
			'June',
			'July',
			'August',
			'September',
			'October',
			'November',
			'December'
		]
		if self.settings.get('english_date', False):
			date = string(days[today.tm_wday], today.tm_mday, months[today.tm_mon-1], today.tm_year, sep=' ')
		elif self.settings.get('american_digit_date', False) == 'simple':
			date = string(today.tm_year, today.tm_mon, today.tm_mday, sep='-')
		elif self.settings.get('american_digit_date', False) == '6 digits':
			date = '-'.join([str(today.tm_year), str(today.tm_mon).rjust(2, '0'), str(today.tm_mday).rjust(2, '0')])
		else:
			date = string(today.tm_mday, today.tm_mon, today.tm_year, sep='-')
		points = [region.begin() for region in self.view.sel()]
		sm('Insert today\'s date')
		for point in points:
			self.view.insert(edit, point, date)

