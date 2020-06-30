'''CssParse - A Simple CSS Parser'''

__version__ = "1.0.0"

class CssParse:
    """A simple CSS style parser.

    It is a fast way to search for selectors and styles.
    """

    def __init__(self):
        pass

    @staticmethod
    def _strip(css) -> str:
        """Strip the CSS string.

        Ensuring cleaning of any extra whitespace.

        Arguments:
            css {str} -- CSS file as a string.

        Returns:
            str -- Stripped CSS string.
        """
        return ''.join(list([char for char in css if char not in list(["\n", "\r", "\t"])]))

    def _format(self, buffer):
        reparsed_buffer = dict()
        formatted_buffer = list()
        output_selector = list()
        if any(brace in buffer for brace in ["{", "}"]):
            reparsed_buffer = self.parse(''.join(buffer))
        else:
            if ";" in buffer:
                formatted_buffer = list(filter(None, "".join(buffer).replace(": ", ":").split(";")))
                output_selector = [value.strip(" ") for value in formatted_buffer if value is not None and value != "" and value != " "]
            else:
                formatted_buffer = "".join(buffer).replace(": ", ":")
                output_selector = list([formatted_buffer])
            output_selector_dict = list()
            for selector in output_selector:
                selector_split = selector.split(":")
                if len(selector_split) == 2:
                    output_selector_dict.append({selector_split[0]: selector_split[1]})
                else:
                    output_selector_dict.append(selector)
        if reparsed_buffer:
            return reparsed_buffer
        else:
            return output_selector_dict

    def parse(self, css) -> dict:
        """Parse the CSS string into a dict of lists.

        Sequentially search a string until { character is found, then write everything after
        that character until the next } character.

        Arguments:
            css {str} -- String of CSS data from external style sheet.

        Returns:
            output dict -- Dict of selector names and styles

            Example:
                margin-bottom:60px;display:block
        """
        assert isinstance(css, str), False
        buffer = list()
        comment = list()
        output = dict()
        if isinstance(css, str):
            css = self._strip(css)
            brace_depth = 0
            key_name = str()
            key_name_comment = str()
            for char_pos, _ in enumerate(css):
                if "/*" in css[char_pos:char_pos+2]:
                    key_name_comment = f"comment ___{char_pos}"
                    output[key_name_comment] = str()
                    comment = list()
                    comment.append(css[char_pos])
                elif "*/" in css[char_pos-2:char_pos]:
                    comment.append(css[char_pos])
                    output[key_name_comment] = ''.join(comment)
                    comment = list()
                elif comment:
                    comment.append(css[char_pos])
                else:
                    if "{" in css[char_pos] and brace_depth == 0:
                        brace_depth += 1
                        temp_suffix = " ___{}".format(char_pos)
                        key_name = str(''.join(buffer)) + temp_suffix
                        output[key_name] = str()
                        buffer = list()
                        continue
                    else:
                        buffer.append(css[char_pos])

                    if "}" in css[char_pos] and brace_depth > 0:
                        brace_depth -= 1
                    elif "{" in css[char_pos] and brace_depth > 0:
                        brace_depth += 1

                    if "}" in css[char_pos] and buffer and brace_depth <= 0:
                        buffer.pop()
                        output[key_name] = self._format(buffer)
                        buffer = list()
                        brace_depth = 0
        return output

def main():
    import json
    css_parser = CssParse()
    parsed_css_file = css_parser.parse(open("git.css").read())
    json_dump = json.dumps(parsed_css_file)
    with open("testparsed.json", "w") as file:
        file.write(json_dump)

if __name__ == "__main__":
    main()
