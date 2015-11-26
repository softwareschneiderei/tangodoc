__author__ = 'marius.elvert@softwareschneiderei.de'

import xml.etree.ElementTree as ET

class XmiParser:

    def parse(self, filename):
        tree = ET.parse(filename);
        root = tree.getroot()
        
        for classinfo in root.findall("classes"):
            print classinfo.attrib["name"]



