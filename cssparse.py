import re

class CssParse:
    """A simple CSS style parser.

    This parses a string and looks for CSS open and close braces. This does not parse
    selector names. It is a fast way to search for styles only.
    """

    def __init__(self):
        self.buffer = []
        self.output = dict()
        self.css = str()

    def __str__(self):
        return str(self.output)

    def __repr__(self):
        return self.output

    def strip(self, css) -> str:
        """Strip the CSS string.

        Ensuring cleaning of any extra whitespace.

        Arguments:
            css {str} -- CSS file as a string.

        Returns:
            str -- Stripped CSS string.
        """
        assert isinstance(css, str), False
        if isinstance(css, str):
            stripped = re.sub(r"[\n\r\t]", "", css)
            stripped = re.sub(r"[\\]{1,6}[nrt]", "", stripped)
            return str(stripped)

    def parse(self, css) -> list:
        """Parse the CSS string into a list of lists.

        Sequentially search a string until { character is found, then write everything after
        that character until the next } character.

        Arguments:
            css {str} -- String of CSS data from external style sheet.

        Returns:
            self.output list -- List of selector styles

            Example:
                margin-bottom:60px;display:block
        """
        assert isinstance(css, str), False
        if not isinstance(css, str):
            return []
        else:
            self.css = self.strip(css)
            b = 0
            key_name = str()
            for _ in enumerate(self.css):
                if "{" in self.css[b]:
                    key_name = str(''.join(self.buffer))
                    self.output[key_name] = str()
                    self.buffer = []
                elif "}" in self.css[b] and self.buffer:
                    self.output[key_name] = set(filter(None, "".join(self.buffer).replace(": ", ":").split(";")))
                    self.output[key_name] = [value.strip(" ") for value in self.output[key_name] if value is not None and value != "" and value != " "]
                    self.buffer = []
                else:
                    self.buffer.append(self.css[b])
                b += 1
            return self.output
