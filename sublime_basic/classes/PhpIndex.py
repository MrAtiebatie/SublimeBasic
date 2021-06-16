import sublime

class PhpIndex:

    """Find existence"""
    def find_symbols(self, entity):
        symbols = sublime.active_window().lookup_symbol_in_index(entity)
        symbols = [entity for entity in symbols if ".php" in entity[0]]

        return list(map(lambda item: item[1], symbols))