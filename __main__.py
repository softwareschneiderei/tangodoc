__author__ = 'vagrant'
import XmiParser
from MarkdownGenerator import MarkdownGenerator

if __name__ == "__main__":
    parser = XmiParser.XmiParser()
    documentationlist = parser.parse("MAXv.xmi")

    with open("doc.md", "wb") as file:
        generator = MarkdownGenerator(file)
        for documentation in documentationlist:
            generator.dump(documentation)
