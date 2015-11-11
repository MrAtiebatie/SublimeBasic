import sublime
import sublime_plugin
from .SublimeBasic import Basic

#--------------------------------------------------------
# Auto Complete Plugin
#--------------------------------------------------------
class BasicAutoComplete:
    def run(self, edit):
        view = self.view

        for sel in view.sel():
            line = view.line(sel.end())
            current_line = view.substr(line)

            tags = open(Basic().project_path() + '.tags', 'r', newline='', encoding='utf-8')
            with tags as inF:
                for line in inF:
                    if 'MaziBox/Services/Dropbox' in line:
                        print(line.strip())
                        return

    def find_defenition(self, variable, location):
        view = sublime.active_window().active_view()

        return [['Social (Hello)'], ['Cache'], ['Http'], ['Logging'], ['Client']]

class BasicAutoCompleteCommand(sublime_plugin.EventListener):
    def on_query_completions(self, view, variable, locations):
        # print(variable, locations)
        autocomplete = BasicAutoComplete()

        for sel in view.sel():
            line = view.line(sel.begin())
            line = view.substr(line)

            print(line)


        return autocomplete.find_defenition(view, variable)