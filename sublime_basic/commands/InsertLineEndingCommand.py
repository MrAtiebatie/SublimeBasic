import re
import sublime
import sublime_plugin

#--------------------------------------------------------
# Insert Line Ending Plugin
#--------------------------------------------------------
class InsertLineEndingCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = sublime.load_settings("SublimeBasic.sublime-settings")
        view = self.view

        # Accepted langs
        langs = settings.get("enabled_languages")

        # Selections
        selections = []

        for sel in view.sel():
            sources = view.scope_name(sel.end()).split(" ")

            # Check if one of the sources contains one of the langs values
            result = filter(lambda element: any(element in source for source in sources), langs)

            if len(list(result)) > 0:
                line = view.line(sel.end())
                current_line = view.substr(line)
                pos = 0;

                # Strip unwanted spaces at the end
                view.replace(edit, line, current_line.rstrip(" "))
                line = view.line(sel.end())

                character = self.choose_character(view, sel)

                # Don't add a character if it's already there
                if current_line.strip().endswith(character.strip()[0]):
                    if " ?>" in view.substr(line):
                        tag = view.substr(line).index(" ?>")
                        pos = view.line(sel.begin()).a + tag
                    else:
                        pos = line.end()
                else:
                    if " ?>" in view.substr(line):
                        # Calculate php end tag index and insert character
                        tag = view.substr(line).index(" ?>")
                        pos = view.line(sel.begin()).a + tag
                        self.view.insert(edit, pos, character.replace('|', ''))
                        pos += self.determine_cursor_position(character)
                    else:
                        self.view.insert(edit, line.end(), character.replace('|', ''))
                        pos = line.end() + self.determine_cursor_position(character)

                selections.append(pos)
            else:
                self.view.insert(edit, sel.end(), ';')
                selections.append(sel.end() + self.determine_cursor_position(';'))

        # Clear current cursors
        view.sel().clear()

        # Set cursors on the end of the line
        for sel in selections:
            view.sel().add(sel)


    def choose_character(self, view, sel):
        """Choose the ending character."""

        scope_bfr  = []
        row, col   = view.rowcol(sel.begin())
        text_point = view.text_point(row, 0)
        line       = view.line(sel.end())

        for col in range(text_point, line.end()):
            scopes = view.scope_name(col).split(' ')
            for scope in scopes:
                if scope not in scope_bfr:
                    scope_bfr.append(scope)

        # Remove None elements
        scope = list(filter(None, scope_bfr))
        scope = " ".join(scope)

        types = {
            ';': [['keyword.operator.assignment'], ['!keyword.control', '!punctuation.separator.key-value.js', 'function-call'], ['punctuation.section.array.end'], ['keyword.control', '!punctuation.section.group.begin.php']],
            ',': [['meta.object-literal.key'], ['meta.array', 'meta.group', 'keyword.operator.key', '!punctuation.section.group.end'], ['meta.array', 'keyword.operator.key'], ['punctuation.separator.key-value.js']],
            ' {|}': [['keyword.control.php meta.group'], ['keyword.control meta.group punctuation.section.group.begin'], ['storage.type.function'], ['keyword.control.conditional'], ['keyword.control.loop']],
        }

        for key, type in types.items():
            for keywords in type:
                conditions = []

                # Compare the scope against the keywords
                for keyword in keywords:
                    if ("!" in keyword and keyword[1:] not in scope):
                        conditions.append(keyword)
                    elif keyword in scope:
                        conditions.append(keyword)

                if len(conditions) == len(keywords):
                    return key

        return ';'


    def determine_cursor_position(self, text):
        # If the text contains a pipe | set the cursor to that position
        if '|' in text:
            return text.index('|')
        else:
            return len(text)