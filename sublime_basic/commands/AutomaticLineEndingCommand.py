import re
import json
import sublime
import sublime_plugin
from ..utils import Utils

#--------------------------------------------------------
# Insert Line Ending Plugin
#--------------------------------------------------------
class AutomaticLineEndingCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = sublime.load_settings("SublimeBasic.sublime-settings")
        view = self.view

        # Accepted langs
        langs = settings.get("enabled_languages")

        for sel in view.sel():
            scope = self.get_current_scope(sel.end())

            block = self.get_block_type(scope)
            line = view.line(sel.end())

            view.sel().clear()
            view.sel().add(line.end())

            print(block)

            if view.substr(line)[-1] != block['character']:
                sublime.active_window().run_command('insert_snippet', { 'contents': block['character'] })

    def get_current_scope(self, sel):
        scope = self.view.scope_name(sel).split(' ')

        return list(filter(None, scope))

    def get_block_type(self, scopes):
        blocks = Utils().file_get_contents(Utils.package_path() + 'sublime_basic/commands/blocks.json', relative=False)
        blocks = json.loads(blocks)

        result = filter(lambda block: any(scope.endswith(block['scope']) for scope in scopes), blocks)
        result = list(result)

        if result:
            return result.pop()
        else:
            return {'character': ';'}
