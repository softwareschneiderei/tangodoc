from __future__ import print_function
import XmiParser
from MarkdownGenerator import MarkdownGenerator
import unicodedata
import string
import sys

def error(*objs):
    print("ERROR: ", *objs, file=sys.stderr)
    sys.exit(1)

def slugify(filename):
    validFilenameChars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    cleanedFilename = unicodedata.normalize('NFKD', unicode(filename, "utf-8")).encode('ASCII', 'ignore')
    return ''.join(c for c in cleanedFilename if c in validFilenameChars)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        error("tangodoc <input-files>")

    parser = XmiParser.XmiParser()

    for input in sys.argv[1:]:
        documentationlist = parser.parse(input)

        for documentation in documentationlist:
            with open("%s.md" % slugify(documentation.name), "wb") as file:
                generator = MarkdownGenerator(file)
                generator.dump(documentation)
