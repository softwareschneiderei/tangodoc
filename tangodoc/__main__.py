from __future__ import print_function
import xmiparser
from markdown_generator import MarkdownGenerator
import unicodedata
import string
import sys


def error(*objs):
    print("ERROR: ", *objs, file=sys.stderr)
    sys.exit(1)


def slugify(base_file_name):
    valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    cleaned_filename = unicodedata.normalize('NFKD', unicode(base_file_name, "utf-8")).encode('ASCII', 'ignore')
    return ''.join(c for c in cleaned_filename if c in valid_filename_chars)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        error("tangodoc <input-files>")

    parser = xmiparser.XmiParser()

    for input_files in sys.argv[1:]:
        documentation_list = parser.parse(input_files)

        for documentation in documentation_list:
            filename = "%s.md" % slugify(documentation.name)
            with open(filename, "wb") as target_file:
                generator = MarkdownGenerator(target_file)
                generator.dump(documentation)
                print("Created %s for device class %s." % (filename, documentation.name))
