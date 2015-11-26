__author__ = 'marius.elvert@softwareschneiderei.de'

class MarkdownGenerator:

    def __init__(self, file):
        self.file = file

    def oneline(self, text):
        return ' '.join(text.splitlines())

    def dump(self, documentation):
        # Write name and description
        self.file.write("# %s\n\n" % documentation.name)

        if documentation.description:
            self.file.write("%s\n" % documentation.description)

        # Write properties
        self.file.write("## Properties\n\n")

        name_width = max(max(map(lambda p: len(p.name), documentation.properties)), len("Name"), 3)
        description_width = max(max(map(lambda p: len(self.oneline(p.description)), documentation.properties)), len("Description"), 3)

        self.file.write("| %s | %s |\n" % ("Name".ljust(name_width), "Description".ljust(description_width)))
        self.file.write("| %s | %s |\n" % ("-"*name_width, "-"*description_width))

        for propertyinfo in documentation.properties:
            self.file.write("| %s | %s |\n" % (propertyinfo.name.ljust(name_width), self.oneline(propertyinfo.description).ljust(description_width)))
