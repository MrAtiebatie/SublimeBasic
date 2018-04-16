import sublime
import sublime_plugin
from ..classes.PhpDependencies import PhpDependencies

#--------------------------------------------------------
# Check namespaces
#--------------------------------------------------------
class CheckNamespacesCommand(sublime_plugin.TextCommand):

    results = []
    definitions = []
    entity = None

    """Constructor"""
    def run(self, edit):
        view = self.view
        php = PhpDependencies()

        dependencies = php.get_dependencies(view)
        imported = php.get_imported_classes(view)

        # Include a possible namespace in the dependencies
        dependencies = list(map(lambda dep: php.include_namespace(view, dep), dependencies))

        # Compare the used classes vs the imported classes
        unimported = php.get_unimported(view, dependencies, imported)

        # Find their file
        unimported = self.lookup_unimported(unimported)

        # We separate the single occurrences from the multiple to show a quick panel
        single = list(filter(lambda item: isinstance(item[1], str), unimported))
        multiple = list(filter(lambda item: isinstance(item[1], list), unimported))

        # Import them
        for result in single:
            self.insert_namespace_from_symbol(result[1], result[0])

        if len(multiple) > 0:
            print(multiple[0])
            self.choose_from_occurrences(multiple[0])

    """Show quick panel"""
    def choose_from_occurrences(self, occurences):
        self.entity = occurences[0]

        occurences.pop(0)

        self.definitions = occurences[0]

        sublime.active_window().show_quick_panel(occurences[0], self.on_done)

    """Insert unimported"""
    def lookup_unimported(self, unimported):
        results = []

        for entity in unimported:
            entity = self.view.substr(entity)

            if "\\" not in entity:
                result = self.find_existence(entity)

                results.append([entity, result])

        return results

    """Find existence"""
    def find_existence(self, entity):
        symbols = sublime.active_window().lookup_symbol_in_index(entity)
        symbols = [entity for entity in symbols if ".php" in entity[0]]

        if len(symbols) == 1:
            return symbols[0][1]
        elif len(symbols) > 1:
            symbols = list(map(lambda item: item[1], symbols))

            return symbols

    """On item selection"""
    def on_done(self, index):
        if index > 0:
            self.insert_namespace_from_symbol(self.definitions[index], self.entity)

            self.view.run_command('check_namespaces')

    """Remove project name from filename"""
    def remove_project_name(self, filename):
        filename = filename.split("/")

        filename.pop(0)

        return "/".join(filename)

    """Insert namespace from symbol"""
    def insert_namespace_from_symbol(self, filename, entity):
        filename = self.remove_project_name(filename)

        sublime.active_window().run_command("insert_namespace", { "item": [entity, filename] })

        self.entity = None