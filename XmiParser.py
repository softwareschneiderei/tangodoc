__author__ = 'marius.elvert@softwareschneiderei.de'

import xml.etree.ElementTree as ET
from Documentation import Documentation

class XmiParser:

    __type_translation_table = {
        "pogoDsl:StringType": "string",
        "pogoDsl:IntType": "integer",
        "pogoDsl:UShortType" : "unsigned short",
        "pogoDsl:UIntType" : "unsigned integer"
    }

    def __translate_type(self, type):
        if type in self.__type_translation_table:
            return self.__type_translation_table[type]
        else:
            return type

    def parse(self, filename):
        tree = ET.parse(filename);
        root = tree.getroot()

        namespace = {'xsi' : 'http://www.w3.org/2001/XMLSchema-instance'}

        for classinfo in root.findall("classes"):

            result = Documentation()
            result.name = classinfo.attrib["name"]
            print classinfo.attrib["name"]

            for propertyinfo in classinfo.findall("deviceProperties"):
                type = self.__translate_type(propertyinfo.find("type").get("{%s}type" % namespace['xsi']))
                default = propertyinfo.find("DefaultPropValue").text
                print "---- PROPERTY ----"
                print " -- %s (type=%s, default=%s)" % (propertyinfo.attrib["name"], type, default)
                print propertyinfo.attrib["description"]
                #result.addproperty(propertyinfo.attrib["name"], propertyinfo.attrib["description"], self.__translate_type(propertyinfo.attrib["type"]), propertyinfo.attrib["default"])

            for commandinfo in classinfo.findall("commands"):
                print "---- COMMAND ----"
                print " -- ", commandinfo.attrib["name"]

