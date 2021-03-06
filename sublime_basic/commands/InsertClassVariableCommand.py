import sublime
import sublime_plugin

#--------------------------------------------------------
# Insert Class Variable Plugin
#--------------------------------------------------------
class InsertClassVariableCommand(sublime_plugin.TextCommand):

    visiblity = '';
    data_type = '';
    comment   = '';

    def run(self, edit):
        self.visiblity = "public"
        self.view.window().show_input_panel('Variable data type:', '', self.type_output, None, None)

    def type_output(self, data_type):
        self.data_type = data_type
        self.view.run_command('insert_variable', {
            'visiblity': self.visiblity,
            'data_type': self.data_type,
            'comment': self.comment
        })

class InsertVariableCommand(sublime_plugin.TextCommand):
    def run(self, edit, visiblity, data_type, comment):
        view = self.view
        sel = view.sel()

        # Get indentation
        indentation = self.get_indentation()

        region = view.find('class (.*)', 0)
        row, col = view.rowcol(region.a)
        selection = view.substr(sel[0])

        if (selection.startswith('$') != True):
            selection = '$' + selection

        view.insert(edit, self.rowcol(row+2), indentation + '/**\n')

        # if comment != None:
        #     view.insert(edit, self.rowcol(row+3), indentation + ' * ' + comment + '\n')

        view.insert(edit, self.rowcol(row+3), indentation + ' * @var ' + data_type + ' ' + selection + '\n')
        view.insert(edit, self.rowcol(row+4), indentation + ' */ \n')
        view.insert(edit, self.rowcol(row+5), indentation + visiblity + ' ' + selection + ';\n\n')

    def get_indentation(self):
        settings = self.view.settings()

        # Get indentation
        use_spaces = settings.get('translate_tabs_to_spaces')
        tab_size = int(settings.get('tab_size', 8))
        indent_characters = '\t'
        if use_spaces:
            indent_characters = ' ' * tab_size

        return indent_characters

    def rowcol(self, row, col=0):
        return self.view.text_point(row, col)