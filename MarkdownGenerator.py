__author__ = 'marius.elvert@softwareschneiderei.de'

class MarkdownGenerator:

    def __init__(self, file):
        self.file = file

    def oneline(self, text):
        return ' '.join(text.splitlines())

    # Each description must be a tuple of the column title and a lambda converting a list element to cell content
    def write_table(self, column_descriptions, list):

        # Markdown requires tables to be at least 3 element wide
        minwidth=3
        column_width = []

        # Find the width of each column
        for description in column_descriptions:
            column_title = description[0]
            column_get = description[1]
            column_content_width = 0
            if len(list) > 0:
                column_content_width = max(map(lambda e : len(self.oneline(column_get(e))), list))
            column_width.append(max(column_content_width, len(column_title), minwidth))

        # Get the titles
        titles = map(lambda d : d[0], column_descriptions)
        # Extend the width to their column widths
        titles = map(lambda s : s[1].ljust(column_width[s[0]]), enumerate(titles))

        # Helper to write columns
        def writecolumn(list): self.file.write("| %s |\n" % ' | '.join(list))

        # Write the header
        writecolumn(titles)
        writecolumn(map(lambda w : "-"*w, column_width))

        # Write the actual content
        for row in list:
            # FIXME: add a newline check
            content = map(lambda e : self.oneline(e[1](row)), column_descriptions)
            content = map(lambda s : s[1].ljust(column_width[s[0]]), enumerate(content))
            writecolumn(content)

        self.file.write("\n")


    def dump(self, documentation):
        # Write name and description
        self.file.write("# %s\n\n" % documentation.name)

        if documentation.description:
            self.file.write("%s\n" % documentation.description)

        # Write properties
        self.file.write("## Properties\n\n")

        propertytable_description = [
            ("Name", lambda p : p.name),
            ("Type", lambda p : p.type),
            ("Default Value", lambda p : p.default),
            ("Description", lambda p : p.description)
        ]
        self.write_table(propertytable_description, documentation.properties)

        self.file.write("## Commands\n\n")

        def writecommandparameter(commandinfo):
            if commandinfo.parametertype=="void":
                return "-"
            return "(%s) - %s" % (commandinfo.parametertype, commandinfo.parameterdescription)

        def writecommandresult(commandinfo):
            if commandinfo.resulttype=="void":
                return "-"
            return "(%s) - %s" % (commandinfo.resulttype, commandinfo.resultdescription)

        commandtable_description = [
            ("Name", lambda p : p.name),
            ("Parameter", writecommandparameter),
            ("Result", writecommandresult),
            ("Description", lambda p : p.description)
        ]

        self.write_table(commandtable_description, documentation.commands)

        self.file.write("## Attributes\n\n")

        attributetable_description = [
            ("Name", lambda p : p.name),
            ("Type", lambda p : p.type),
            ("Description", lambda p : p.description)
        ]

        self.write_table(attributetable_description, documentation.attributes)