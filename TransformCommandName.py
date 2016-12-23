# here's a little plugin for sublime. With this, you can transform your 
# plugin's name to the right name to write in the file `Key Bindings User` for example
# It's toogle.

# use :
# select a plugin name, for example, `MyPluginForSublimeCommand`, and find in the command panel Transform Command Name then press Enter.
# You have now my_plugin_for_sublime. Like I said, it's toogle, so you can select the one in underscore_case end transform it in the
# camelCaseCommand by doing the same thing !

# Warning : For have the command in the command pannel, you MUST download the file math2001.sublime-commands

import sublime, sublime_plugin, re

class TransformCommandNameCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		def md(t):
			sublime.message_dialog(str(t))

		for selection in self.view.sel():
			# on recupere le texte de la selection
			if selection.empty():
				s = sublime.get_clipboard()
			else:
				s = self.view.substr(selection)

			if '_' not in s:
				# ca veut dire qu'il n'y a pas _, donc on doit le transformer pour qu'il soit valable dans le fichier de raccourci
				# ex: il etait : UnNomDePlugin
				#	  il devient : un_nom_de_plugin

				# on rajoute un _ devant chaque majuscule
				underscore_case = re.sub(r'([A-Z])', r'_\1', s)

				# on le met tout en minuscule
				underscore_case = underscore_case.lower()

				# on supprime le premier _ (_nom_de_votre_command_avant_ca)
				if underscore_case[0] == '_':
					underscore_case = underscore_case.replace('_', '', 1)

				# on split le texte tout les _
				underscore_case = underscore_case.split('_')

				# pour pouvoir retirer le "command" a la fin
				if (underscore_case[-1] == 'command'):
					del(underscore_case[-1]) # l'index -1 recupere le dernier element de la liste

				# on le re assemble avec des _
				underscore_case = '_'.join(underscore_case)

				new_text = underscore_case


			else:
				# il y a des underscore, donc on doit le transformer pour qu'il soit un nom de plugin valable
				
				# on split le texte tout les _
				texte = s.split('_')

				camelCase = ''
				for mot in texte:
					camelCase += mot.capitalize()

				camelCase += 'Command'

				new_text = camelCase

			# on remplace la selection par notre texte modifie !
			if selection.empty():
				self.view.insert(edit, selection.begin(), new_text)
			else:
				self.view.replace(edit, selection, new_text)