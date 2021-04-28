import re
import markdown
from googletrans import Translator


class StoryLine:
    def __init__(self, line):
        self.line = line
        self.regex_macro = r"""\$([\w]*)"""
        self.compiled = re.compile(self.regex_macro)

    def exec(self, environment):

        for match in re.finditer(self.regex_macro, self.line, re.DOTALL):
            self.line = self.line.replace(match.group(0), str(environment[match.group(1)]))

        if environment['lang'] == "eng":
            self.line = environment["translator"].translate(self.line, dest='en').text

        self.line = markdown.markdown(self.line)

    def is_empty(self):
        return self.line == ""

    def __str__(self):
        return self.line

    def to_json(self):
        return {'line' : self.line}
