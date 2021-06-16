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

        #-------------------------------------------------
        # Undocumented feature
        # print(view.extract_tokens_with_scopes(region))
        # ------------------------------------------------

        # Accepted langs
        langs = settings.get("enabled_languages")

        for sel in view.sel():
            scope = self.get_current_scope(sel.end())

            block = self.get_block_type(scope)
            line = view.line(sel.end())

            view.sel().clear()
            view.sel().add(line.end())

            if view.substr(line)[-1] != block['character']:
                sublime.active_window().run_command('insert_snippet', { 'contents': block['character'] })

    # Get current scope
    def get_current_scope(self, sel):
        scope = self.view.scope_name(sel).split(' ')

        return list(filter(None, scope))

    # Sort by index
    def sort_by_index(self, block, scope):
        return scope.find(block['scope'])

    # Get block type and character
    def get_block_type(self, scopes):
        blocks = Utils().file_get_contents(Utils.package_path() + 'sublime_basic/commands/blocks.json', relative=False)
        blocks = json.loads(blocks)

        scopes.reverse()
        scope = ' '.join(scopes)

        # print('\n', scope, '\n')

        # result = filter(lambda block: any(block['scope'] in scope for scope in scopes), blocks)
        blocks = filter(lambda block: scope.find(block['scope']) >= 0, blocks)
        result = sorted(blocks, key=lambda block: self.sort_by_index(block, scope))
        result = list(result)

        # print('\n', result)

        if result:
            return result.pop(0)
        else:
            return {'character': ';'}
