"""Contains functionality needed for identifying and parsing html tags"""

import cgi
from collections import defaultdict
from HTMLParser import HTMLParser

def _wrap_tag(tag):
    return '<code class=\"tag-%s">%s</code>' % (tag, cgi.escape(tag))

def _wrap_attrs(attrs):
    wrapped = ''
    if attrs:
        for key, value in attrs:
            wrapped += ' ' + key + ('="%s"' % value if value else '')
    return cgi.escape(wrapped)

def _enclose_in_angle_brackets(string):
    return cgi.escape('<') + string + cgi.escape('>')

class TagHighlighter(HTMLParser):
    r"""Parses html and emits escaped html with wrapped tags

    Incoming html will be escaped and produced as output contained in
    formatted_html, with the following exception:

    A tag with name TAG will be wrapped in a non-escaped span, which will have a
    class of 'tag-' followed by TAG. Note that, for efficiency, the output will
    be a list of parsed segments.

    tag_to_count will be a dict containing mappings from each encountered tag to
    the number of each encountered.

    Examples:
    >>> marked_up_html = TagHighlighter('''
    ... <body>
    ...   <p>Unclosed tag
    ...   <form>
    ...     <label>Form input<label>
    ...     <input name="form_input" type="text" class="required">
    ...   <form>
    ... <body>
    ... ''')
    >>> marked_up_html.formatted_html
    ['\n', '&lt;<code class="tag-body">body</code>&gt;', '\n  ', '&lt;<code class="tag-p">p</code>&gt;', 'Unclosed tag\n  ', '&lt;<code class="tag-form">form</code>&gt;', '\n    ', '&lt;<code class="tag-label">label</code>&gt;', 'Form input', '&lt;<code class="tag-label">label</code>&gt;', '\n    ', '&lt;<code class="tag-input">input</code> name="form_input" type="text" class="required"&gt;', '\n  ', '&lt;<code class="tag-form">form</code>&gt;', '\n', '&lt;<code class="tag-body">body</code>&gt;', '\n']
    >>> marked_up_html.tag_to_count
    defaultdict(<type 'int'>, {'body': 2, 'p': 1, 'input': 1, 'form': 2, 'label': 2})

    """

    def __init__(self, html):
        HTMLParser.__init__(self)

        self.formatted_html = []
        self.tag_to_count = defaultdict(int)
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.tag_to_count[tag] += 1
        self.formatted_html.append(
            _enclose_in_angle_brackets(_wrap_tag(tag) + _wrap_attrs(attrs)))

    def handle_endtag(self, tag):
        self.tag_to_count[tag] += 1
        self.formatted_html.append(_enclose_in_angle_brackets(_wrap_tag(tag)))

    def handle_startendtag(self, tag, attrs):
        self.tag_to_count[tag] += 1
        self.formatted_html.append(_enclose_in_angle_brackets(
            _wrap_tag(tag) + _wrap_attrs(attrs) + cgi.escape(" /")))

    def handle_data(self, data):
        self.formatted_html.append(cgi.escape(data))

    def handle_entityref(self, name):
        self.formatted_html.append(cgi.escape(name))

    def handle_charref(self, name):
        self.formatted_html.append(cgi.escape(name))

    def handle_comment(self, data):
        self.formatted_html.append(cgi.escape(data))

    def handle_decl(self, decl):
        self.formatted_html.append(
            _enclose_in_angle_brackets(cgi.escape("!" + decl)))

    def handle_pi(self, data):
        self.formatted_html.append(cgi.escape("?" + data))

    def unknown_decl(self, data):
        self.formatted_html.append(
            _enclose_in_angle_brackets(cgi.escape("![" + data + "]")))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
