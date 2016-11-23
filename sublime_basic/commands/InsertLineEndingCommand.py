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

                # Don't add a semicolon if it's already there
                if character in current_line:
                    if " ?>" in view.substr(line):
                        tag = view.substr(line).index(" ?>")
                        pos = view.line(sel.begin()).a + tag
                    else:
                        pos = line.end()
                else:
                    if " ?>" in view.substr(line):
                        # Calculate php end tag index and insert semicolon
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

        # print(view.substr(view.line(text_point)))

        for col in range(text_point, sel.end()):
            scopes = view.scope_name(col).split(' ')
            for scope in scopes:
                if scope not in scope_bfr:
                    scope_bfr.append(scope)

        scope = list(filter(None, scope_bfr))

        # print(scope)

        statements = ['keyword.control.php meta.group.php', 'storage.type.function.php']
        lists = ['meta.object-literal.key.js', 'meta.array.php', 'meta.group.php keyword.operator.key.php']

        if 'keyword.operator.assignment' in scope:
            return ';'
        elif 'function-call' in scope:
            return ';'
        elif [l for l in lists if l in scope]:
            return ','
        elif [s for s in statements if s in scope]:
            return ' {|}'
        elif 'meta.block' in scope:
            return ';'
        else:
            return ';'


    def determine_cursor_position(self, text):
        # If the text contains a pipe | set the cursor to that position
        if '|' in text:
            return text.index('|')
        else:
            return len(text)