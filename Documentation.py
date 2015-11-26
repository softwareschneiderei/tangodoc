__author__ = 'marius.elvert@softwareschneiderei.de'


class Documentation:
    class PropertyInfo:
        def __init__(self, name, description, type, default):
            self.name = ""
            self.description = ""
            self.type = ""
            self.default = ""

    def __init__(self):
        self.name = ""
        self.description = ""
        self.properties = []

    def addproperty(self, name, description, type, default):
        self.properties.append(Documentation.PropertyInfo(name, description, type, default))
