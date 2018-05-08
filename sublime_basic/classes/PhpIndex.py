import sublime

class PhpIndex:

    """Find existence"""
    def find_symbols(self, entity):
        symbols = sublime.active_window().lookup_symbol_in_index(entity)
        symbols = [entity for entity in symbols if ".php" in entity[0]]

        if len(symbols) == 1:
            return symbols[0][1]
        elif len(symbols) > 1:
            return list(map(lambda item: item[1], symbols))