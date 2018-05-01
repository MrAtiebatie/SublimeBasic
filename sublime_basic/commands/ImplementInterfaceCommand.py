import re
import sublime
import sublime_plugin
from ..utils import Utils
import ctagsplugin as ctags

#--------------------------------------------------------
# Implement Interface Plugin
# @todo implement class detection
#--------------------------------------------------------
class ImplementInterfaceCommand(sublime_plugin.TextCommand):

    files = []
    content = ''
    interfaces = []

    def run(self, edit):
        edit = edit
        view = self.view
        window = sublime.active_window()
        self.interfaces = []

        content = Utils().get_full_view(view)
        tags_file = ctags.find_tags_relative_to(
            view.file_name(), ctags.setting('tag_file'))

        # Target scope
        inheriteds = view.find_by_selector("entity.other.inherited-class.php")
        implements = view.find_by_selector("storage.modifier.implements.php")
        aliasses   = view.find_by_selector("keyword.other.use-as.php")

        for entity in inheriteds:
            scope = view.scope_name(entity.begin())
            if not "meta.use.php" in scope:
                # Filter the parent class
                if entity.end() > implements[0].begin():
                    interface = view.substr(entity)

                    namespace = self.get_interface_namespace(content, interface)
                    self.interfaces.append([interface, (namespace or "")])

        window.show_quick_panel(self.interfaces, self.choose_interface)

    # Choose which interface to implement
    def choose_interface(self, item):
        if item == -1:
            return

        window = sublime.active_window()
        interface = self.interfaces[item]

        self.files = window.lookup_symbol_in_index(interface)
        self.files = [item[1] for item in self.files]

        window.show_quick_panel(self.files, self.choose_file)

    # Choose which interface from which file
    def choose_file(self, file):
        if file == -1:
            return

        file = self.files[file]
        view = sublime.active_window().active_view()

        contract = Utils.file_get_contents(file)

        class_methods = self.get_class_methods(self.content)
        contract_methods = self.get_interface_methods(contract)
        missing_methods = []

        # Here we calculate the difference between the required methods
        # from the interface and the actual class methods
        for method in contract_methods:
            if not any(m in method for m in class_methods):
                missing_methods.append(method)

                if len(missing_methods) is 0:
                    sublime.message_dialog('Required interface methods already implemented.')

                    for method in missing_methods:
                        view.run_command('insert_method', {'content': method})

    # Get class name
    def get_class_name(self, content):
        return re.findall('class ([a-zA-Z]+)', content, re.MULTILINE)

    # Get interface namespace
    def get_interface_namespace(self, content, interface):
        regex = r'use ([a-zA-Z\\]+)[\sas\s?]+' + interface + ';'
        matches = re.findall(regex, content)

        if len(matches) > 0:
            return matches[0]
        else:
            return None

    # Get first element
    def get_first(self, array):
        if len(array) > 0:
            return array[0]

    # Get class methods
    def get_class_methods(self, content):
        # @todo get method comments with the following regex: (\/\*([^*]|[\s]|\*+[^*\/]|[\s])*\*\/)
        methods = re.findall('([public |static |abstract |protected |private ]+function [^)]+\))', content, re.MULTILINE)
        result = []

        if len(methods) > 0:
            for match in methods:
                result.append(match.strip())

        return result

    # Get interface methods
    def get_interface_methods(self, content):
        methods = re.findall('[ ]+(/\*\*(?:\s.+)+[\s]+[public |static |abstract |protected |private ]+function [^)]+\))', content, re.MULTILINE)
        result = []

        if len(methods) > 0:
            for match in methods:
                result.append(match.strip())

        return result

# Insert the methods
class InsertMethodCommand(sublime_plugin.TextCommand):
    def run(self, edit, content):
        class_ending = view.find_all('[}]')

        if len(class_ending) > 0:
            class_ending = class_ending[-1]
            row, col = view.rowcol(class_ending.a)

            self.view.insert(edit, view.text_point(row, col), "\n\t" + content + "\n\t{\n\n\t}\n")