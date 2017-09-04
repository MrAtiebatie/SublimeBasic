import re
import sublime
import sublime_plugin
from ..utils import Utils

#--------------------------------------------------------
# Wrap text in function
#--------------------------------------------------------
class PromptWrapTextCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window = sublime.active_window()

        window.run_command('hide_panel')
        window.show_input_panel('Function:', '', self.on_done, None, None)

    def on_done(self, function):
        self.view.run_command('wrap_text', { 'text': function })


class WrapTextCommand(sublime_plugin.TextCommand):
    def run(self, edit, text):
        view = self.view

        for sel in view.sel():
            string = view.substr(sel)
            view.replace(edit, sel, text + '(' + string + ')')
