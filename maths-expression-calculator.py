import sublime, sublime_plugin
import os
import re
from math import *

r = sqrt

# 4 + 5

def md(*t, **kwargs):
	t = kwargs.get('sep', ' ').join([str(el) for el in t])
	sublime.message_dialog(t)

def sm(*t, **kwargs):
	t = kwargs.get('sep', ' ').join([str(el) for el in t])
	sublime.status_message(t)

def em(*t, **kwargs):
	t = kwargs.get('sep', ' ').join([str(el) for el in t])
	sublime.error_message(t)

def quote(s):
	return '"{}"'.format(s)

def replace(view, region, text):
	region = [region.a, region.b]
	view.run_command('fm_edit_replace')


# tester("some arg", 0.5 + 0.5 * 5)

class Region(sublime.Region):


	def __get_nb(self, s):
		return int(''.join(s[1:]))

	def begin(self, new=None):

		if new is None:
			return sublime.Region(self)

		if type(new) == int:
			self.a = new

		if type(new) == str:
			new = new.strip()
			exec("self.a {}= {}".format(new[0], self.__get_nb(new)))

	def end(self, new=None):
		if new is None:
			return sublime.Region(self)

		if type(new) == int:
			self.b = new

		if type(new) == str:
			new = new.strip()
			exec("self.b {}= {}".format(new[0], self.__get_nb(new)))

	def __init__(self, *args, **kwargs):
		self.from_region(*args)

	def from_region(self, a, b=1):
		if type(a) == sublime.Region:
			self.a, self.b = a.a, a.b
		else:
			self.a, self.b = a, b
		return self

	def get_region(self):
		return sublime.Region(self.a, self.b)


class MathsExpressionCalculatorCommand(sublime_plugin.TextCommand):

	def get_setting(self, name, default=None):
		return self.settings.get(name) or default

	def __replace(self, region):

		region = Region(region)

		expression = self.view.substr(region)
		expression, diff = self.__remove_lonely_bracket(expression)
		if expression[0] == ' ': region.begin('+1')
		if expression[-1] == ' ': region.end('-1')

		region.end('-' + str(diff))

		try:
			result = eval(expression)
		except Exception as e:
			em('maths_expression_calculator: Unable to run the expression \n{}\n. Error message: {} '.format(repr(str(expression)), e.msg))
		else:
			if type(result) == float and result.is_integer(): result = int(result)
			if self.replace_expression:
				self.view.replace(self.edit, region.get_region(), str(result))
			else:
				self.view.insert(self.edit, region.get_region().end(), " = " + str(result))

	def __is_an_expression_char(self, char):
		return char in self.ok_chars_list

	def __remove_lonely_bracket(self, exp):
		opening = exp.count('(')
		closing = exp.count(')')
		if opening == closing:
			return exp, 0

		remove = True
		new = ''
		if opening > closing:
			for char in exp:
				if not remove or char != '(':
					new += char
				elif remove:
					remove = False
		else:
			for char in exp[::-1]:
				if not remove or char != ')':
					new += char
				elif remove:
					remove = False
			new = new[::-1]

		return new, abs(opening - closing)

	def run(self, edit, *args, **kwargs):
		self.edit = edit
		self.window = self.view.window()
		self.selection = sublime.Selection(self.view.id())
		self.settings = self.view.settings()

		self.replace_expression = kwargs.get('replace_expression', True)

		v = self.view
		self.ok_chars_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '/', '*',
		'(', ')', '.', ' ', 'r']
		for region in v.sel():
			line = v.substr(v.line(region.begin()))
			keep_moving_backwards = True
			if region.empty():
				start = region.begin() - 1
				end = start + 1 # for the beginning
				char = ''
				while keep_moving_backwards:
					char = v.substr(start)
					if self.__is_an_expression_char(char) is False:
						keep_moving_backwards = False
						start += 1
					else:
						start -= 1
				keep_moving_forwards = True
				while keep_moving_forwards:
					char = v.substr(end)
					if self.__is_an_expression_char(char) is False:
						keep_moving_forwards = False
					else:
						end += 1
				self.__replace(sublime.Region(start, end))
			else:
				# if there is a selection, then I consider it as the expression
				# for char in self.view.substr(region):
				# 	if self.__is_an_expression_char(char) is False:
				# 		return em('Wrong expression: the char {} is not correct!'.format(repr(char)))

				self.__replace(region)
