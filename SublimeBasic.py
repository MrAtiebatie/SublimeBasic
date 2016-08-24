import sys
import imp
import sublime_plugin
from .sublime_basic.commands.ImplementInterfaceCommand import ImplementInterfaceCommand
from .sublime_basic.commands.InsertClassVariableCommand import InsertClassVariableCommand
from .sublime_basic.commands.InsertClassVariableCommand import InsertVariableCommand
from .sublime_basic.commands.InsertFileTemplateCommand import InsertFileTemplateCommand
from .sublime_basic.commands.InsertLineEndingCommand import InsertLineEndingCommand
from .sublime_basic.commands.NewPhpClassCommand import NewPhpClassCommand
from .sublime_basic.events.HtmlSourceAutoComplete import HtmlSourceAutoComplete

# Dependecy reloader for SublimeBasic plugin
# The original idea is borrowed from
# https://github.com/wbond/sublime_package_control/blob/master/package_control/reloader.py

# class ReloadModulesCommand(sublime_plugin.EventListener):
    # def on_post_save(self, view):
reload_mods = []
for mod in sys.modules:
    if mod.startswith('SublimeBasic') and sys.modules[mod] != None:
        reload_mods.append(mod)

mods_load_order = [
    'SublimeBasic.sublime_basic.commands.ImplementInterfaceCommand',
    'SublimeBasic.sublime_basic.commands.InsertClassVariableCommand',
    'SublimeBasic.sublime_basic.commands.InsertClassVariableCommand',
    'SublimeBasic.sublime_basic.commands.InsertFileTemplateCommand',
    'SublimeBasic.sublime_basic.commands.InsertLineEndingCommand',
    'SublimeBasic.sublime_basic.commands.NewPhpClassCommand',
    'SublimeBasic.sublime_basic.events.HtmlSourceAutoComplete'
]

for mod in mods_load_order:
    if mod in reload_mods:
        m = sys.modules[mod]
        if 'on_module_reload' in m.__dict__:
            m.on_module_reload()
        imp.reload(sys.modules[mod])