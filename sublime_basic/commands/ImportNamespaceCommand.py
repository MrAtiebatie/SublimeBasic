import re
import sublime
import sublime_plugin
import ctagsplugin as ctags
from subprocess import Popen, PIPE
from ..utils import Utils

#--------------------------------------------------------
# Import namespace
#--------------------------------------------------------
class ImportNamespaceCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        tags_file = ctags.find_tags_relative_to(
            view.file_name(), ctags.setting('tag_file'))

        for sel in view.sel():
            symbol = view.substr(view.word(sel.begin()))

            result = ctags.JumpToDefinition.run(symbol, None, "", [], view, tags_file)

            filename  = result[0][0].filename
            classname = result[0][0].symbol

            contents  = Utils().file_get_contents(filename)
            namespace = re.findall('namespace ([^\s]+);', contents, re.MULTILINE)

            if namespace:
                self.namespace = namespace[0] + "\\" + classname
                self.insert_use_among_others(edit)

    def insert_use_among_others(self, edit):
        regions = self.view.find_all(r"^(use\s+.+[;])", 0)
        if len(regions) > 0:
            region = regions[0]
            for r in regions:
                region = region.cover(r)

            self.view.replace(edit, region, self.build_uses())
            sublime.status_message('Successfully imported ' + self.namespace)

    def build_uses(self):
        uses = []
        use_stmt = "use " + self.namespace + ";"

        self.view.find_all(r"^(use\s+.+[;])", 0, '$1', uses)
        uses.append(use_stmt)
        uses = list(set(uses))
        uses.sort(key = len)

        return "\n".join(uses)