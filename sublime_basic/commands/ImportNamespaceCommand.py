import re
import sublime
import sublime_plugin
import ctagsplugin as ctags
from ..utils import Utils
from subprocess import Popen, PIPE

#--------------------------------------------------------
# Import namespace
#--------------------------------------------------------
class ImportNamespaceCommand(sublime_plugin.TextCommand):
    results = []
    edit = None

    def run(self, edit):
        view = self.view

        # We require SublimeText/CTags
        if not "find_tags_relative_to" in dir(ctags):
            sublime.error_message("CTags methods not available. Please install SublimeText/CTags")
            return

        # Find tags file
        tags_file = ctags.find_tags_relative_to(view.file_name(), ctags.setting("tag_file"))

        # List definitions
        not_found = []
        symbols = []

        # For each selection in the current view
        for sel in view.sel():
            symbol = view.substr(view.word(sel.begin()))

            if symbol in symbols:
                continue

            symbols.append(symbol)

            # Find definition and filter the unnessecary keys
            results = ctags.JumpToDefinition.run(symbol, None, "", [], view, tags_file)

            # If results is more than one
            if results != None:
                results = list(map(lambda x: [x.symbol, x.filename], results[0]))
                if len(results) > 1 and len(view.sel()) == 1:
                    # Show selection panel
                    self.results = results
                    sublime.active_window().show_quick_panel(results, self.on_done)
                elif len(results) > 1 and len(view.sel()) > 1:
                    not_found.append(symbol)
                else:
                    sublime.active_window().run_command("insert_namespace", { "item": results[0] })
            else:
                sublime.status_message("No definitions found for " + symbol)

        if len(not_found) > 0:
            sublime.message_dialog("Could not import the following classes because of multiple occurences.\n\n - " + "\n - ".join(not_found))

    def on_done(self, index):
        """ ON NAMESPACE SELECTION """
        if index == -1:
            return

        result = self.results[index]
        sublime.active_window().run_command("insert_namespace", { "item": result })

class InsertNamespaceCommand(sublime_plugin.TextCommand):
    def run(self, edit, item):
        """ INSERT AND ORDER THE NAMESPACES """
        classname = item[0]
        filename  = item[1]

        contents  = Utils().file_get_contents(filename)
        namespace = re.findall("namespace ([^\s]+);", contents, re.MULTILINE)

        if namespace:
            namespace = namespace[0] + "\\" + classname
        else:
            namespace = classname

        regions = self.view.find_all(r"^(use\s+.+[;])", 0)
        if len(regions) > 0:
            region = regions[0]
            for r in regions:
                region = region.cover(r)

            self.view.replace(edit, region, self.build_uses(namespace))
            sublime.status_message("Successfully imported " + namespace)
        else:
            region = self.view.find_by_selector("keyword.other.namespace.php")

            row, col = self.view.rowcol(region[0].begin())
            region   = self.view.text_point(row + 2, col)

            self.view.insert(edit, region, self.build_uses(namespace) + "\n\n")
            sublime.status_message("Successfully imported " + namespace)

    def build_uses(self, namespace):
        """ BUILD USE STATEMENTS """
        uses = []
        use_stmt = "use " + namespace + ";"

        self.view.find_all(r"^(use\s+.+[;])", 0, "$1", uses)
        uses.append(use_stmt)
        uses = list(set(uses))
        uses.sort(key = len)

        return "\n".join(uses)