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
            column_width.append(max(max(map(lambda e : len(column_get(e)), list)), len(column_title), minwidth))

        print "widths: ", column_width

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
            content = map(lambda e : e[1](row), column_descriptions)
            content = map(lambda s : s[1].ljust(column_width[s[0]]), enumerate(content))
            writecolumn(content)


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
            ("Description", lambda p : self.oneline(p.description))
        ]
        self.write_table(propertytable_description, documentation.properties)
'''
        name_width = max(max(map(lambda p: len(p.name), documentation.properties)), len("Name"), 3)
        description_width = max(max(map(lambda p: len(self.oneline(p.description)), documentation.properties)), len("Description"), 3)

        self.file.write("| %s | %s |\n" % ("Name".ljust(name_width), "Description".ljust(description_width)))
        self.file.write("| %s | %s |\n" % ("-"*name_width, "-"*description_width))

        for propertyinfo in documentation.properties:
            self.file.write("| %s | %s |\n" % (propertyinfo.name.ljust(name_width), self.oneline(propertyinfo.description).ljust(description_width)))
'''