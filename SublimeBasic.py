import sys
import sublime_plugin
from imp import reload
from .sublime_basic.commands.ImplementInterfaceCommand import ImplementInterfaceCommand
from .sublime_basic.commands.InsertClassVariableCommand import InsertClassVariableCommand
from .sublime_basic.commands.InsertClassVariableCommand import InsertVariableCommand
from .sublime_basic.commands.InsertFileTemplateCommand import InsertFileTemplateCommand
from .sublime_basic.commands.InsertLineEndingCommand import InsertLineEndingCommand
from .sublime_basic.commands.NewPhpClassCommand import NewPhpClassCommand

class ReloadModulesCommand(sublime_plugin.EventListener):
	def on_post_save(self, view):
		reload_mods = []
		for mod in sys.modules:
			if mod.startswith('SublimeBasic') and sys.modules[mod] != None:
				reload_mods.append(mod)

		for mod in reload_mods:
			print(mod)
			reload(sys.modules[mod])